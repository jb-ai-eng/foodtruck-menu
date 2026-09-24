import os
import textwrap
import urllib.parse
from datetime import datetime
import streamlit as st

# =========================================================
# CONFIGURACIÓN DEL NEGOCIO & DATOS REALES
# =========================================================
NOMBRE_NEGOCIO = "Victor's Fast Food"
ESLOGAN = "⚡ High-Performance Street Food | Sabor Urbano Premium"
INSTAGRAM = "victorsfast_food"
WHATSAPP_PHONE = "584249367077"
DELIVERY_FEE = 3.00
DIRECCION_LOCAL = "Food Truck Victor's Fast Food — Punto Central"

DATOS_PAGO = {
    "pago_movil": {
        "banco": "Banesco",
        "telefono": "0424-9367077",
        "cedula": "20.505.294",
        "titular": "Hugo Victor",
    },
    "binance": {
        "email": "Hugo_victor_17@hotmail.com"
    },
    "efectivo": {
        "detalle": "Billetes de $ USD en buen estado. Indicar denominación para el cambio."
    }
}

CATEGORIAS = [
    {"id": "todos", "nombre": "⚡ Todo el Menú"},
    {"id": "hamburguesas", "nombre": "🍔 Hamburguesas"},
    {"id": "perros", "nombre": "🌭 Perros Calientes"},
    {"id": "enrollados", "nombre": "🌯 Enrollados & Pepitos"},
    {"id": "sandwiches", "nombre": "🥪 Sandwiches & Club House"},
    {"id": "extras", "nombre": "🍟 Salchipapas & Extras"},
    {"id": "bebidas", "nombre": "🥤 Bebidas Frías"},
]

MENU_ITEMS = [
    # --- HAMBURGUESAS ---
    {
        "id": "hamb_sencilla",
        "categoria": "hamburguesas",
        "nombre": "Hamburguesa Sencilla",
        "precio": 6.00,
        "descripcion": "Pan artesanal, carne smash premium, lechuga, tomate, cebolla, papitas crujientes y queso amarillo fundido.",
        "badge": "🥩 Clásica",
        "emoji": "🍔"
    },
    {
        "id": "hamb_carne",
        "categoria": "hamburguesas",
        "nombre": "Hamburguesa de Carne",
        "precio": 8.00,
        "descripcion": "Carne de res jugosa, tocineta ahumada crujiente, jamón, queso americano, huevo frito, vegetales y papitas.",
        "badge": "🔥 Favorita",
        "emoji": "🍔"
    },
    {
        "id": "hamb_pollo",
        "categoria": "hamburguesas",
        "nombre": "Hamburguesa de Pollo",
        "precio": 8.00,
        "descripcion": "Pechuga de pollo a la plancha marinada, tocineta, jamón, queso americano, huevo, vegetales y papitas.",
        "badge": "🍗 Pechuga",
        "emoji": "🍔"
    },
    {
        "id": "hamb_chuleta",
        "categoria": "hamburguesas",
        "nombre": "Hamburguesa Chuleta",
        "precio": 8.00,
        "descripcion": "Chuleta ahumada seleccionada, tocineta, jamón, queso americano, huevo, vegetales frescos y papitas.",
        "badge": "🍖 Ahumada",
        "emoji": "🍔"
    },
    {
        "id": "hamb_crispy",
        "categoria": "hamburguesas",
        "nombre": "Hamburguesa Crispy",
        "precio": 8.50,
        "descripcion": "Pollo empanizado ultra crujiente dorado, tocineta, jamón, queso amarillo, vegetales y papas.",
        "badge": "⚡ Extra Crunch",
        "emoji": "🍔"
    },
    {
        "id": "hamb_doble_mixta",
        "categoria": "hamburguesas",
        "nombre": "Hamburguesa Doble / Mixta",
        "precio": 15.00,
        "descripcion": "Doble proteína a tu elección (carne/pollo/chuleta), doble tocineta, jamón, queso americano, huevo y papitas.",
        "badge": "👑 Best Seller",
        "emoji": "🍔"
    },

    # --- PERROS CALIENTES ---
    {
        "id": "dog_pequeno",
        "categoria": "perros",
        "nombre": "Perro Pequeño",
        "precio": 2.50,
        "descripcion": "Pan suave, salchicha nacional, lechuga, tomate picadito, cebolla, queso amarillo, papitas y salsa de la casa.",
        "badge": "🥖 Street Style",
        "emoji": "🌭"
    },
    {
        "id": "dog_sencillo",
        "categoria": "perros",
        "nombre": "Perro Sencillo",
        "precio": 3.50,
        "descripcion": "Pan grande, salchicha nacional, lechuga, tomate, cebolla, queso amarillo, lluvia de papitas y salsas.",
        "badge": "⭐ El Más Pedido",
        "emoji": "🌭"
    },
    {
        "id": "dog_especial",
        "categoria": "perros",
        "nombre": "Perro Especial",
        "precio": 5.00,
        "descripcion": "Pan grande, salchicha nacional, jamón, tocineta crujiente, huevo, queso amarillo fundido y vegetales.",
        "badge": "🥓 Con Todo",
        "emoji": "🌭"
    },
    {
        "id": "dog_polaco",
        "categoria": "perros",
        "nombre": "Perro Polaco",
        "precio": 8.00,
        "descripcion": "Pan grande, salchicha polaca premium, tocineta crocante, jamón, queso amarillo derretido, huevo y vegetales.",
        "badge": "👑 Especialidad",
        "emoji": "🌭"
    },

    # --- ENROLLADOS & PEPITOS ---
    {
        "id": "enrollado_carne",
        "categoria": "enrollados",
        "nombre": "Enrollado de Carne",
        "precio": 20.00,
        "descripcion": "Carne tierna salteada, jamón, queso, tocineta, huevo, lechuga, tomate, cebolla y papitas crujientes.",
        "badge": "🌯 Gigante",
        "emoji": "🌯"
    },
    {
        "id": "enrollado_pollo",
        "categoria": "enrollados",
        "nombre": "Enrollado de Pollo",
        "precio": 20.00,
        "descripcion": "Pollo jugoso en cubos, jamón, queso, tocineta, huevo, lechuga, tomate, cebolla y papitas.",
        "badge": "🌯 Para Compartir",
        "emoji": "🌯"
    },
    {
        "id": "enrollado_mixto",
        "categoria": "enrollados",
        "nombre": "Enrollado Mixto",
        "precio": 20.00,
        "descripcion": "Combinación perfecta de carne y pollo, jamón, queso, tocineta, huevo y aderezos especiales.",
        "badge": "🔥 Mixto Top",
        "emoji": "🌯"
    },
    {
        "id": "pepito_mixto",
        "categoria": "enrollados",
        "nombre": "Pepito Mixto Especial",
        "precio": 25.00,
        "descripcion": "Pan baguette extra largo con carne y pollo abundantes, jamón, tocineta, huevo, queso fundido y papitas.",
        "badge": "👑 El Monstruo",
        "emoji": "🥖"
    },
    {
        "id": "mini_pepito",
        "categoria": "enrollados",
        "nombre": "Mini Pepito",
        "precio": 10.00,
        "descripcion": "Carne salteada, vegetales seleccionados, tocineta, queso amarillo y papitas en porción individual.",
        "badge": "🎯 Personal",
        "emoji": "🥖"
    },

    # --- SANDWICHES & CLUB HOUSE ---
    {
        "id": "club_house",
        "categoria": "sandwiches",
        "nombre": "Club House 4 Pisos",
        "precio": 12.00,
        "descripcion": "Cuatro pisos de pan tostado con pollo jugoso, jamón, queso amarillo, huevo, vegetales y papas fritas.",
        "badge": "🥪 4 Niveles",
        "emoji": "🥪"
    },
    {
        "id": "sand_granjero",
        "categoria": "sandwiches",
        "nombre": "Sandwich Granjero",
        "precio": 10.00,
        "descripcion": "Pan tipo granjero horneado, pechuga de pollo, lechuga, tomate, cebolla, queso amarillo y papas fritas.",
        "badge": "🌾 Granjero",
        "emoji": "🥪"
    },

    # --- SALCHIPAPAS & EXTRAS ---
    {
        "id": "salchipapa",
        "categoria": "extras",
        "nombre": "Salchipapa Extrema",
        "precio": 15.00,
        "descripcion": "Montaña de papas fritas doradas, abundante salchicha en rodajas, lluvia de queso y baño de salsas.",
        "badge": "🍟 Para 2 o 3",
        "emoji": "🍟"
    },
    {
        "id": "papa_500",
        "categoria": "extras",
        "nombre": "Ración de Papa 500gr",
        "precio": 5.00,
        "descripcion": "Medio kilo de papas fritas premium crujientes al punto de sal.",
        "badge": "🍟 Familiar",
        "emoji": "🍟"
    },
    {
        "id": "papa_250",
        "categoria": "extras",
        "nombre": "Ración de Papa 250gr",
        "precio": 2.50,
        "descripcion": "Porción individual de papas fritas doraditas y crujientes.",
        "badge": "🍟 Individual",
        "emoji": "🍟"
    },
    {
        "id": "tequenos",
        "categoria": "extras",
        "nombre": "Ración de Tequeños (6u)",
        "precio": 5.00,
        "descripcion": "Tequeños crujientes rellenos de queso derretido con salsa tártara de ajo artesanal.",
        "badge": "🧀 Favoritos",
        "emoji": "🧀"
    },

    # --- BEBIDAS ---
    {
        "id": "nestea",
        "categoria": "bebidas",
        "nombre": "Nestea Frío con Limón",
        "precio": 2.00,
        "descripcion": "Vaso frío de té helado con el punto perfecto de limón refrescante.",
        "badge": "🧊 Con Hielo",
        "emoji": "🍹"
    },
    {
        "id": "refresco_botellita",
        "categoria": "bebidas",
        "nombre": "Refresco Botellita",
        "precio": 1.00,
        "descripcion": "Refresco personal helado (Coca-Cola, Pepsi, Hit, Chinotto).",
        "badge": "🥤 Helado",
        "emoji": "🥤"
    },
    {
        "id": "refresco_1l",
        "categoria": "bebidas",
        "nombre": "Refresco 1.0L",
        "precio": 2.00,
        "descripcion": "Botella de 1 Litro fría para compartir en grupo.",
        "badge": "🍾 Familiar",
        "emoji": "🍾"
    }
]

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title=f"{NOMBRE_NEGOCIO} | Digital Ordering Terminal",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Estilos CSS globales
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Outfit:wght@600;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }

    .stApp {
        background: #08090C;
        color: #FFFFFF;
    }

    header, footer {visibility: hidden;}

    /* Badge visuales */
    .badge-tag {
        background: rgba(229, 37, 33, 0.2);
        border: 1px solid #E52521;
        color: #FF5A50;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
        display: inline-block;
    }

    .price-tag {
        font-family: 'Outfit', sans-serif;
        font-size: 22px;
        font-weight: 900;
        color: #FFD000;
    }

    /* Botón de envío a WhatsApp */
    .wa-btn {
        display: block;
        width: 100%;
        text-align: center;
        background: #25D366;
        color: #000000 !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 900;
        font-size: 16px;
        padding: 14px 20px;
        border-radius: 14px;
        text-decoration: none;
        margin-top: 15px;
        text-transform: uppercase;
        box-shadow: 0 5px 20px rgba(37, 211, 102, 0.4);
    }
    .wa-btn:hover {
        background: #20ba5a;
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# ESTADO REACTIVO DEL CARRITO
# ---------------------------------------------------------
if "carrito" not in st.session_state:
    st.session_state["carrito"] = {}

def agregar_item(item_id, item_nombre, item_precio):
    actual = st.session_state["carrito"].get(item_id, {"cantidad": 0, "especificaciones": ""})
    nueva_cant = actual["cantidad"] + 1
    st.session_state["carrito"][item_id] = {
        "nombre": item_nombre,
        "precio": item_precio,
        "cantidad": nueva_cant,
        "subtotal": nueva_cant * item_precio,
        "especificaciones": actual.get("especificaciones", "").strip() or "Estándar (Con todo)",
    }

def quitar_item(item_id):
    if item_id in st.session_state["carrito"]:
        actual = st.session_state["carrito"][item_id]
        if actual["cantidad"] > 1:
            nueva_cant = actual["cantidad"] - 1
            st.session_state["carrito"][item_id]["cantidad"] = nueva_cant
            st.session_state["carrito"][item_id]["subtotal"] = nueva_cant * actual["precio"]
        else:
            del st.session_state["carrito"][item_id]

def actualizar_especificaciones(item_id, notas):
    if item_id in st.session_state["carrito"]:
        st.session_state["carrito"][item_id]["especificaciones"] = notas.strip() if notas else "Estándar (Con todo)"

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

col_h_logo, col_h_info = st.columns([1, 4])
with col_h_logo:
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown("# 🍔")

with col_h_info:
    st.title(NOMBRE_NEGOCIO)
    st.caption(f"{ESLOGAN} | 📸 Instagram: @{INSTAGRAM}")

st.divider()

# ---------------------------------------------------------
# COLUMNAS: MENÚ (IZQ) Y PEDIDO (DER)
# ---------------------------------------------------------
col_menu, col_order = st.columns([1.6, 1.1], gap="large")

# =========================================================
# MENÚ DE PLATILLOS (NATIVO STREAMLIT)
# =========================================================
with col_menu:
    st.subheader("🔥 Menú Digital")

    nombres_tabs = [cat["nombre"] for cat in CATEGORIAS]
    tabs = st.tabs(nombres_tabs)

    for i, tab in enumerate(tabs):
        cat_id = CATEGORIAS[i]["id"]
        with tab:
            platillos = MENU_ITEMS if cat_id == "todos" else [p for p in MENU_ITEMS if p["categoria"] == cat_id]

            c_left, c_right = st.columns(2)
            for idx, plato in enumerate(platillos):
                target_col = c_left if idx % 2 == 0 else c_right

                with target_col:
                    pid = plato["id"]
                    p_nombre = plato["nombre"]
                    p_precio = plato["precio"]
                    p_desc = plato["descripcion"]
                    p_badge = plato["badge"]
                    p_emoji = plato["emoji"]

                    item_en_carrito = st.session_state["carrito"].get(pid, {})
                    qty_actual = item_en_carrito.get("cantidad", 0)

                    # Contenedor con borde nativo
                    with st.container(border=True):
                        st.markdown(f"### {p_emoji} {p_nombre}")
                        st.markdown(f"<span class='badge-tag'>{p_badge}</span>", unsafe_allow_html=True)
                        st.write(p_desc)
                        st.markdown(f"<div class='price-tag'>${p_precio:.2f}</div>", unsafe_allow_html=True)

                        if qty_actual == 0:
                            if st.button(f"⚡ AGREGAR +${p_precio:.2f}", key=f"add_{cat_id}_{pid}", use_container_width=True):
                                agregar_item(pid, p_nombre, p_precio)
                                st.rerun()
                        else:
                            st.success(f"✓ {qty_actual} en pedido")
                            c_sub, c_add = st.columns(2)
                            with c_sub:
                                if st.button("➖ Quitar", key=f"sub_{cat_id}_{pid}", use_container_width=True):
                                    quitar_item(pid)
                                    st.rerun()
                            with c_add:
                                if st.button("➕ Sumar", key=f"sum_{cat_id}_{pid}", use_container_width=True):
                                    agregar_item(pid, p_nombre, p_precio)
                                    st.rerun()

                            specs = st.text_input(
                                "Detalles (ej. sin cebolla):",
                                value=item_en_carrito.get("especificaciones", ""),
                                key=f"spec_{cat_id}_{pid}"
                            )
                            if specs != item_en_carrito.get("especificaciones", ""):
                                actualizar_especificaciones(pid, specs)

# =========================================================
# CARRITO Y CHECKOUT
# =========================================================
with col_order:
    st.subheader("⚡ Tu Pedido")

    carrito = st.session_state["carrito"]

    if not carrito:
        st.info("Tu orden está vacía. Agrega platillos desde el menú.")
    else:
        subtotal_orden = sum(d["subtotal"] for d in carrito.values())

        for pid, datos in list(carrito.items()):
            with st.container(border=True):
                st.write(f"**{datos['cantidad']}x {datos['nombre']}** — ${datos['subtotal']:.2f}")
                st.caption(f"📝 {datos['especificaciones']}")

        if st.button("🗑️ Vaciar Pedido", use_container_width=True):
            st.session_state["carrito"] = {}
            st.rerun()

        st.divider()

        # Configuración de Entrega
        modalidad = st.radio(
            "Tipo de Entrega:",
            [f"🛵 Delivery (+${DELIVERY_FEE:.2f})", "🏃 Pick-Up / Retiro", "🍽️ Comer en el Local"],
            key="mod_entrega"
        )

        costo_envio = DELIVERY_FEE if "Delivery" in modalidad else 0.0
        if "Delivery" in modalidad:
            direccion_entrega = st.text_area("Dirección exacta:", key="dir_envio")
        elif "Local" in modalidad:
            direccion_entrega = st.text_input("Número de Mesa:", key="mesa_envio")
        else:
            direccion_entrega = "Retiro directo en local"

        # Métodos de Pago
        metodo_pago = st.radio("Método de Pago:", ["📱 Pago Móvil", "🟡 Binance Pay", "💵 Efectivo ($ USD)"], key="met_pago")

        referencia_pago = ""
        if "Pago Móvil" in metodo_pago:
            pm = DATOS_PAGO["pago_movil"]
            st.info(f"**Pago Móvil Banesco**\n- Teléfono: {pm['telefono']}\n- Cédula: {pm['cedula']}\n- Titular: {pm['titular']}")
            referencia_pago = st.text_input("Número de Referencia:", key="ref_pm")
        elif "Binance" in metodo_pago:
            st.info(f"**Binance Pay**\nCorreo: {DATOS_PAGO['binance']['email']}")
            referencia_pago = st.text_input("ID / Correo Binance:", key="ref_bn")
        else:
            st.info(DATOS_PAGO['efectivo']['detalle'])
            referencia_pago = st.text_input("Denominación del billete (para cambio):", key="ref_ef")

        # Datos del cliente
        cliente_nombre = st.text_input("Nombre Completo:", key="cli_nom")
        cliente_telefono = st.text_input("Teléfono de Contacto:", key="cli_tel")

        total_final = subtotal_orden + costo_envio

        st.markdown(f"### Total: **${total_final:.2f}**")

        # Validación
        listo = True
        if not cliente_nombre:
            st.warning("Escribe tu nombre.")
            listo = False
        elif "Delivery" in modalidad and not direccion_entrega:
            st.warning("Indica la dirección de entrega.")
            listo = False

        if listo:
            ticket_msg = f"🧾 *TICKET DE PEDIDO — {NOMBRE_NEGOCIO.upper()}*\n"
            ticket_msg += f"👤 Cliente: {cliente_nombre}\n"
            ticket_msg += f"📱 Teléfono: {cliente_telefono}\n"
            ticket_msg += f"📍 Modo: {modalidad}\n"
            ticket_msg += f"🏠 Destino: {direccion_entrega}\n"
            ticket_msg += "--------------------------------\n"
            for datos in carrito.values():
                ticket_msg += f"• {datos['cantidad']}x {datos['nombre']} (${datos['subtotal']:.2f})\n"
                ticket_msg += f"  Notas: {datos['especificaciones']}\n"
            ticket_msg += "--------------------------------\n"
            ticket_msg += f"Subtotal: ${subtotal_orden:.2f}\n"
            ticket_msg += f"Delivery: ${costo_envio:.2f}\n"
            ticket_msg += f"*TOTAL: ${total_final:.2f}*\n"
            ticket_msg += f"Pago: {metodo_pago} (Ref/Detalle: {referencia_pago})\n"

            url_wa = f"https://api.whatsapp.com/send?phone={WHATSAPP_PHONE}&text={urllib.parse.quote(ticket_msg)}"

            st.markdown(
                f"""
                <a href="{url_wa}" target="_blank" class="wa-btn">
                    📲 TRANSMITIR PEDIDO POR WHATSAPP
                </a>
                """,
                unsafe_allow_html=True
            )