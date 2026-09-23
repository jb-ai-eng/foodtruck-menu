import json
import os
import urllib.parse
import streamlit as st

# 1. Configuración de la página
st.set_page_config(
    page_title="Food Truck - Menú Digital", page_icon="🛞", layout="centered"
)

USUARIOS_FILE = "usuarios.json"


# Funciones para manejo de usuarios
def cargar_usuarios():
    if not os.path.exists(USUARIOS_FILE):
        return {}
    with open(USUARIOS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def guardar_usuario(usuario, password, telefono):
    usuarios = cargar_usuarios()
    usuarios[usuario] = {"password": password, "telefono": telefono}
    with open(USUARIOS_FILE, "w") as f:
        json.dump(usuarios, f, indent=4)


# Inicializar variables de sesión
if "usuario_logueado" not in st.session_state:
    st.session_state["usuario_logueado"] = None

# ---------------------------------------------------------
# BARRA LATERAL (OPCIONAL: INICIAR SESIÓN / REGISTRO)
# ---------------------------------------------------------
with st.sidebar:
    st.header("👤 Mi Cuenta")

    if st.session_state["usuario_logueado"]:
        st.success(f"Sesión activa: **{st.session_state['usuario_logueado']}**")
        if st.button("Cerrar Sesión"):
            st.session_state["usuario_logueado"] = None
            st.rerun()
    else:
        st.info("Iniciar sesión es opcional, ¡puedes pedir directamente!")
        opcion_cuenta = st.radio(
            "Acceso:", ["Ver Menú sin Cuenta", "Iniciar Sesión", "Registrarse"]
        )

        usuarios = cargar_usuarios()

        if opcion_cuenta == "Iniciar Sesión":
            u_input = st.text_input("Usuario")
            p_input = st.text_input("Contraseña", type="password")
            if st.button("Ingresar"):
                if (
                    u_input in usuarios
                    and usuarios[u_input]["password"] == p_input
                ):
                    st.session_state["usuario_logueado"] = u_input
                    st.success(f"¡Hola {u_input}!")
                    st.rerun()
                else:
                    st.error("Datos incorrectos.")

        elif opcion_cuenta == "Registrarse":
            nuevo_u = st.text_input("Crear Usuario")
            nuevo_p = st.text_input("Crear Contraseña", type="password")
            tel = st.text_input("Teléfono")
            if st.button("Crear Cuenta"):
                if nuevo_u in usuarios:
                    st.error("El usuario ya existe.")
                elif not nuevo_u or not nuevo_p:
                    st.error("Completa los campos.")
                else:
                    guardar_usuario(nuevo_u, nuevo_p, tel)
                    st.success("¡Cuenta creada! Ya puedes iniciar sesión.")

# ---------------------------------------------------------
# PÁGINA PRINCIPAL: CATÁLOGO DIGITAL (VISIBLE PARA TODOS)
# ---------------------------------------------------------
st.title("🛞 Food Truck - Menú Digital")
st.write(
    "¡Bienvenido! Selecciona tus platillos favoritos y envía tu pedido por WhatsApp."
)
st.divider()

# Menú con imágenes (puedes reemplazar las URLs por fotos reales del negocio)
menu = {
    "Hot Dog Clásico": {
        "precio": 5.00,
        "desc": "Salchicha premium, cebolla picada, papitas ralladas y salsas de la casa.",
        "foto": "https://images.unsplash.com/photo-1619740455993-9e612b1af08a?w=500",
    },
    "Hot Dog Especial": {
        "precio": 7.50,
        "desc": "Con doble tocino crujiente, queso fundido, cebolla caramelizada y maíz.",
        "foto": "https://images.unsplash.com/photo-1627308595229-7830a5c91f9f?w=500",
    },
    "Papas Fritas": {
        "precio": 3.50,
        "desc": "Papas doradas y sazonadas, servidas con salsa de ajo.",
        "foto": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=500",
    },
    "Soda / Refresco": {
        "precio": 2.00,
        "desc": "Lata de 355ml helada (Coca-Cola, Sprite, Fanta).",
        "foto": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500",
    },
}

carrito = {}

# Desplegar los productos en el menú
st.header("📋 Nuestros Platillos")

for producto, info in menu.items():
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(info["foto"], use_container_width=True)

    with col2:
        st.subheader(f"{producto} - ${info['precio']:.2f}")
        st.write(info["desc"])
        cant = st.number_input(
            f"Cantidad de {producto}",
            min_value=0,
            max_value=15,
            value=0,
            key=producto,
        )
        if cant > 0:
            carrito[producto] = {
                "cantidad": cant,
                "subtotal": cant * info["precio"],
            }

    st.divider()

# ---------------------------------------------------------
# SECCIÓN DE CONFIRMACIÓN Y ENVÍO A WHATSAPP
# ---------------------------------------------------------
st.header("🛒 Confirmar Pedido")

if carrito:
    total = sum(item["subtotal"] for item in carrito.values())
    st.subheader(f"Total a pagar: ${total:.2f}")

    # Si tiene sesión iniciada, usamos su nombre guardado; si no, le pedimos un nombre
    if st.session_state["usuario_logueado"]:
        nombre_cliente = st.session_state["usuario_logueado"]
        st.success(f"Realizando pedido a nombre de: **{nombre_cliente}**")
    else:
        nombre_cliente = st.text_input("Tu Nombre Completo:")

    direccion_mesa = st.text_input(
        "📍 Número de Mesa o Dirección de Entrega:"
    )

    if st.button("📲 Enviar Pedido a WhatsApp", type="primary"):
        if not nombre_cliente:
            st.error("Por favor ingresa tu nombre.")
        elif not direccion_mesa:
            st.error("Por favor ingresa tu número de mesa o dirección.")
        else:
            TELEFONO_DUENO = (
                "13051234567"  # Reemplazar por el WhatsApp real con código de país
            )

            msg = f"👋 *Nuevo Pedido de {nombre_cliente}*\n"
            msg += f"📍 Ubicación/Mesa: {direccion_mesa}\n\n"
            msg += "*Detalle del pedido:*\n"

            for item, datos in carrito.items():
                msg += f"• {datos['cantidad']}x {item} (${datos['subtotal']:.2f})\n"

            msg += f"\n💰 *Total a Pagar:* ${total:.2f}"

            link_wa = f"https://wa.me/{TELEFONO_DUENO}?text={urllib.parse.quote(msg)}"

            st.balloons()
            st.success("¡Tu pedido está listo!")
            st.markdown(
                f"[👉 **Haz clic aquí para abrir WhatsApp y enviar la orden**]({link_wa})"
            )
else:
    st.info("Selecciona al menos un producto arriba para armar tu pedido.")