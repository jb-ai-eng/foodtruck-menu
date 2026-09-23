import json
import os
import urllib.parse
import streamlit as st

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y DISEÑO / COLORES
# ---------------------------------------------------------
st.set_page_config(
    page_title="Food Truck - Menú Digital", page_icon="🛞", layout="centered"
)

# Estilos CSS personalizados (Colores cálidos para Food Truck: Naranja / Rojo / Fondo Suave)
st.markdown(
    """
    <style>
    /* Fondo general */
    .stApp {
        background-color: #FAFAFA;
    }
    /* Encabezados principal */
    h1 {
        color: #D32F2F !important;
        font-family: 'Trebuchet MS', sans-serif;
    }
    h2, h3 {
        color: #E65100 !important;
    }
    /* Tarjetas de productos */
    .stContainer {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    /* Botón principal (WhatsApp) */
    div.stButton > button:first-child {
        background-color: #25D366 !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border-radius: 10px !important;
        border: none !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 2. DATOS RECTIFICABLES DEL NEGOCIO (¡CÁMBIALOS AQUÍ!)
# ---------------------------------------------------------
NOMBRE_FOOD_TRUCK = "🔥 La Esquina Street Food"
TELEFONO_WHATSAPP = (
    "13051234567"  # Cambiar por el número real con código de país (ej: 1305...)
)
DIRECCION_TRUCK = "📍 1234 NW 36th St, Miami, FL 33142"
HORARIO_ATENCION = "⏰ Miércoles a Domingo: 5:00 PM - 12:00 AM"

USUARIOS_FILE = "usuarios.json"


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


if "usuario_logueado" not in st.session_state:
    st.session_state["usuario_logueado"] = None

# ---------------------------------------------------------
# BARRA LATERAL (DATOS DEL TRUCK + CUENTA OPCIONAL)
# ---------------------------------------------------------
with st.sidebar:
    st.title("ℹ️ Información")
    st.write(f"**Ubicación:**\n{DIRECCION_TRUCK}")
    st.write(f"**Horario:**\n{HORARIO_ATENCION}")
    st.write(f"**Teléfono:**\n+{TELEFONO_WHATSAPP}")

    st.divider()
    st.header("👤 Mi Cuenta (Opcional)")

    if st.session_state["usuario_logueado"]:
        st.success(f"Sesión activa: **{st.session_state['usuario_logueado']}**")
        if st.button("Cerrar Sesión"):
            st.session_state["usuario_logueado"] = None
            st.rerun()
    else:
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
# ENCABEZADO Y MENÚ INTERACTIVO
# ---------------------------------------------------------
st.title(NOMBRE_FOOD_TRUCK)
st.caption(f"{DIRECCION_TRUCK} | {HORARIO_ATENCION}")
st.write(
    "¡Elige lo que quieres comer, arma tu pedido y envíalo directo a nuestro WhatsApp!"
)
st.divider()

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

st.header("📋 Menú de Hoy")

for producto, info in menu.items():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(info["foto"], use_container_width=True)
    with col2:
        st.subheader(f"{producto} — ${info['precio']:.2f}")
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
# INTERACCIÓN DEL CLIENTE (CARRITO Y CONFIRMACIÓN)
# ---------------------------------------------------------
st.header("🛒 Tu Pedido")

if carrito:
    total = sum(item["subtotal"] for item in carrito.values())

    # Resumen visual
    st.subheader(f"Total estimado: ${total:.2f}")

    if st.session_state["usuario_logueado"]:
        nombre_cliente = st.session_state["usuario_logueado"]
        st.info(f"Cliente: **{nombre_cliente}**")
    else:
        nombre_cliente = st.text_input(
            "Tu Nombre:", placeholder="Ej. Carlos Pérez"
        )

    direccion_mesa = st.text_input(
        "Mesa # o Nombre para entregar:", placeholder="Ej. Mesa 4 / Para llevar"
    )

    if st.button("📲 Enviar Pedido por WhatsApp"):
        if not nombre_cliente:
            st.error("Ingresa tu nombre para saber quién pide.")
        elif not direccion_mesa:
            st.error("Ingresa el número de mesa o si es para llevar.")
        else:
            msg = f"👋 *NUEVO PEDIDO - {NOMBRE_FOOD_TRUCK}*\n"
            msg += f"👤 *Cliente:* {nombre_cliente}\n"
            msg += f"📍 *Mesa/Entrega:* {direccion_mesa}\n\n"
            msg += "📝 *Detalle del Pedido:*\n"

            for item, datos in carrito.items():
                msg += f"• {datos['cantidad']}x {item} (${datos['subtotal']:.2f})\n"

            msg += f"\n💰 *TOTAL A PAGAR:* ${total:.2f}\n"
            msg += f"\n📍 *Ubicación del Local:* {DIRECCION_TRUCK}"

            link_wa = f"https://wa.me/{TELEFONO_WHATSAPP}?text={urllib.parse.quote(msg)}"

            st.balloons()
            st.success("¡Pedido armado correctamente!")
            st.markdown(
                f"""
                <a href="{link_wa}" target="_blank">
                    <button style="background-color:#25D366; color:white; padding:15px 25px; border:none; border-radius:10px; font-size:18px; width:100%; cursor:pointer;">
                        👉 Toca aquí para enviar a WhatsApp
                    </button>
                </a>
                """,
                unsafe_allow_html=True,
            )
else:
    st.info("Agrega platillos arriba para ver tu resumen de compra.")