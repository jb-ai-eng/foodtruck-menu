import json
import os
import urllib.parse
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Food Truck Menu", page_icon="🛞", layout="centered"
)

USUARIOS_FILE = "usuarios.json"


def cargar_usuarios():
    if not os.path.exists(USUARIOS_FILE):
        return {}
    with open(USUARIOS_FILE, "r") as f:
        return json.load(f)


def guardar_usuario(usuario, password, telefono):
    usuarios = cargar_usuarios()
    usuarios[usuario] = {"password": password, "telefono": telefono}
    with open(USUARIOS_FILE, "w") as f:
        json.dump(usuarios, f, indent=4)


if "usuario_logueado" not in st.session_state:
    st.session_state["usuario_logueado"] = None

st.title("🛞 Food Truck - Menú Digital")

if st.session_state["usuario_logueado"] is None:
    st.subheader("Accede a tu cuenta para ordenar")

    opcion = st.radio(
        "Selecciona una opción:", ["Iniciar Sesión", "Registrarse"]
    )
    usuarios = cargar_usuarios()

    if opcion == "Registrarse":
        nuevo_user = st.text_input("Usuario (Ej. jesus123)")
        nuevo_pass = st.text_input("Contraseña", type="password")
        telefono = st.text_input("Número de Teléfono")

        if st.button("Crear cuenta"):
            if nuevo_user in usuarios:
                st.error("El nombre de usuario ya existe. Elige otro.")
            elif not nuevo_user or not nuevo_pass:
                st.error("Por favor completa los campos.")
            else:
                guardar_usuario(nuevo_user, nuevo_pass, telefono)
                st.success(
                    "¡Cuenta creada con éxito! Ahora puedes Iniciar Sesión."
                )

    elif opcion == "Iniciar Sesión":
        user_input = st.text_input("Usuario")
        pass_input = st.text_input("Contraseña", type="password")

        if st.button("Ingresar"):
            if (
                user_input in usuarios
                and usuarios[user_input]["password"] == pass_input
            ):
                st.session_state["usuario_logueado"] = user_input
                st.success(f"Bienvenido de nuevo, {user_input}!")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")

else:
    st.sidebar.write(
        f"👤 Sesión activa: **{st.session_state['usuario_logueado']}**"
    )
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["usuario_logueado"] = None
        st.rerun()

    st.header("📋 Nuestro Menú")

    menu = {
        "Hot Dog Clásico": 5.00,
        "Hot Dog Especial (Tocino + Queso)": 7.50,
        "Papas Fritas": 3.00,
        "Soda 355ml": 2.00,
    }

    carrito = {}
    for producto, precio in menu.items():
        cant = st.number_input(
            f"{producto} (${precio:.2f})", min_value=0, max_value=10, value=0
        )
        if cant > 0:
            carrito[producto] = {"cantidad": cant, "subtotal": cant * precio}

    direccion = st.text_input("📍 Dirección de entrega / Mesa:")

    if st.button("📲 Confirmar y Enviar Pedido por WhatsApp"):
        if not carrito:
            st.error("Agrega al menos un producto al carrito.")
        elif not direccion:
            st.error("Por favor ingresa la dirección o número de mesa.")
        else:
            TELEFONO_DUENO = "13051234567"  # Cámbialo después por el número real

            total = sum(item["subtotal"] for item in carrito.values())
            msg = f"👋 *Nuevo Pedido de {st.session_state['usuario_logueado']}*\n"
            msg += f"📍 Ubicación: {direccion}\n\n"
            msg += "*Detalle del pedido:*\n"

            for item, datos in carrito.items():
                msg += f"• {datos['cantidad']}x {item} (${datos['subtotal']:.2f})\n"

            msg += f"\n💰 *Total:* ${total:.2f}"

            link_wa = f"https://wa.me/{TELEFONO_DUENO}?text={urllib.parse.quote(msg)}"

            st.success("¡Pedido listo para enviar!")
            st.markdown(
                f"[👉 **Haz clic aquí para enviar el pedido por WhatsApp**]({link_wa})"
            )