import base64
import os
import urllib.parse
from datetime import datetime
import streamlit as st

# =========================================================
# CONFIGURACIÓN DEL NEGOCIO Y ENLACES OFICIALES
# =========================================================
NOMBRE_NEGOCIO = "Victor's Fast Food"
INSTAGRAM_HANDLE = "victorsfast_food"
INSTAGRAM_URL = "https://www.instagram.com/victorsfast_food/"
MAPS_URL = "https://maps.app.goo.gl/5bpuKC6FEBdsTkFM8"
WHATSAPP_PHONE = "584249367077"
DELIVERY_FEE = 3.00

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
        "badge": "🥖 Clásico",
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
    }
]

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title=f"{NOMBRE_NEGOCIO} | Menú Oficial",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# BÚSQUEDA Y CODIFICACIÓN EN BASE64 DEL LOGO Y IMÁGENES
# ---------------------------------------------------------
base_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(base_dir, ".."))

logo_path = None
for posible in [
    os.path.join(base_dir, "assets", "logo.jpg"),
    os.path.join(base_dir, "assets", "logo.png"),
    os.path.join(base_dir, "logo.jpg"),
    os.path.join(base_dir, "logo.png"),
    os.path.join(root_dir, "logo.jpg"),
    os.path.join(root_dir, "logo.png"),
]:
    if os.path.exists(posible):
        logo_path = posible
        break

bg_css = "background-color: #0A0A0A;"
if logo_path:
    with open(logo_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    ext = "png" if logo_path.endswith(".png") else "jpeg"
    bg_css = f"""
        background: linear-gradient(rgba(10, 10, 10, 0.85), rgba(10, 10, 10, 0.92)),
                    url("data:image/{ext};base64,{encoded_string}") no-repeat center center fixed !important;
        background-size: cover !important;
    """

# Estilos CSS
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800;900&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Poppins', sans-serif;
    }}

    .stApp {{
        {bg_css}
        color: #FFFFFF;
    }}

    header, footer {{visibility: hidden;}}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(15, 15, 20, 0.85) !important;
        backdrop-filter: blur(12px) saturate(180%);
        border: 1px solid rgba(229, 27, 36, 0.4) !important;
        border-radius: 18px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }}

    .ig-button {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
        color: #FFFFFF !important;
        padding: 10px 22px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 14px;
        text-decoration: none;
        box-shadow: 0 4px 15px rgba(220, 39, 67, 0.4);
        transition: transform 0.2s ease;
    }}
    .ig-button:hover {{ transform: scale(1.05); }}

    .map-button {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #E51B24 0%, #B30006 100%);
        color: #FFFFFF !important;
        padding: 10px 22px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 14px;
        text-decoration: none;
        box-shadow: 0 4px 15px rgba(229, 27, 36, 0.4);
        transition: transform 0.2s ease;
    }}
    .map-button:hover {{ transform: scale(1.05); }}

    .badge-tag {{
        background-color: rgba(229, 27, 36, 0.25);
        border: 1px solid #E51B24;
        color: #FF5A50;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 6px;
    }}

    .price-tag {{
        font-size: 22px;
        font-weight: 900;
        color: #FFC72C;
        margin-top: 4px;
    }}

    .wa-btn {{
        display: block;
        width: 100%;
        text-align: center;
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
        color: #FFFFFF !important;
        font-weight: 900;
        font-size: 17px;
        padding: 16px;
        border-radius: 16px;
        text-decoration: none;
        margin-top: 15px;
        text-transform: uppercase;
        box-shadow: 0 6px 20px rgba(37, 211, 102, 0.4);
    }}

    div.stButton > button {{
        border-radius: 12px !important;
        font-weight: 700 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# ESTADO DEL CARRITO
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
        "especificaciones": actual.get("especificaciones", "").strip() or "Con todo",
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
        st.session_state["carrito"][item_id]["especificaciones"] = notas.strip() if notas else "Con todo"

# ---------------------------------------------------------
# HEADER: LOGO, REDES Y UBICACIÓN
# ---------------------------------------------------------
col_l, col_c, col_r = st.columns([1, 2, 1])
with col_c:
    if logo_path:
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown(f"<h1 style='text-align:center; color:#FFC72C;'>{NOMBRE_NEGOCIO}</h1>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align: center; margin-top: -10px; margin-bottom: 15px; display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
            <a href="{INSTAGRAM_URL}" target="_blank" class="ig-button">
                <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                </svg>
                Síguenos @{INSTAGRAM_HANDLE}
            </a>
            <a href="{MAPS_URL}" target="_blank" class="map-button">
                📍 Ver Ubicación en Google Maps
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# SECCIÓN GALERÍA DE INSTAGRAM Y FOTOS
# ---------------------------------------------------------
with st.expander("📸 Ver Fotos del Menú & Especialidades Oficiales", expanded=False):
    st.markdown("<p style='text-align:center; color:#AAA;'>Descubre nuestras especialidades reales recién hechas:</p>", unsafe_allow_html=True)
    
    # Busca la foto tanto en la carpeta raíz como en assets
    foto_comida_path = None
    for f_posible in [
        os.path.join(root_dir, "fotos_comida.jpg"),
        os.path.join(root_dir, "fotos_comida.png"),
        os.path.join(base_dir, "fotos_comida.jpg"),
        os.path.join(base_dir, "assets", "fotos_comida.jpg"),
    ]:
        if os.path.exists(f_posible):
            foto_comida_path = f_posible
            break

    if foto_comida_path:
        st.image(foto_comida_path, caption="🍔 Hamburguesa Crispy · 🥪 Club House · 🌯 Pepito Mixto", use_container_width=True)
    else:
        st.warning("Subiendo la vista previa de las imágenes...")

    st.markdown(
        f"""
        <div style="text-align:center; margin-top:10px;">
            <a href="{INSTAGRAM_URL}" target="_blank" class="ig-button">
                📸 Ver más fotos y vídeos en Instagram @{INSTAGRAM_HANDLE}
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# ---------------------------------------------------------
# ESTRUCTURA PRINCIPAL: CATÁLOGO Y PROCESO DE PAGO
# ---------------------------------------------------------
col_menu, col_order = st.columns([1.6, 1.1], gap="large")

# =========================================================
# COLUMNA IZQUIERDA: CATÁLOGO
# =========================================================
with col_menu:
    st.markdown("<h2 style='color:#FFC72C;'>🔥 Menú de Platillos</h2>", unsafe_allow_html=True)

    tabs = st.tabs([c["nombre"] for c in CATEGORIAS])

    for idx_tab, tab in enumerate(tabs):
        cat_id = CATEGORIAS[idx_tab]["id"]
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

                    with st.container(border=True):
                        st.markdown(f"#### {p_emoji} {p_nombre}")
                        st.markdown(f"<span class='badge-tag'>{p_badge}</span>", unsafe_allow_html=True)
                        st.caption(p_desc)
                        st.markdown(f"<div class='price-tag'>${p_precio:.2f}</div>", unsafe_allow_html=True)

                        if qty_actual == 0:
                            if st.button(f"➕ Agregar", key=f"add_{cat_id}_{pid}", use_container_width=True):
                                agregar_item(pid, p_nombre, p_precio)
                                st.rerun()
                        else:
                            st.success(f"✓ {qty_actual} en el carrito")
                            c_sub, c_add = st.columns(2)
                            with c_sub:
                                if st.button("➖ Quitar", key=f"sub_{cat_id}_{pid}", use_container_width=True):
                                    quitar_item(pid)
                                    st.rerun()
                            with c_add:
                                if st.button("➕ Más", key=f"sum_{cat_id}_{pid}", use_container_width=True):
                                    agregar_item(pid, p_nombre, p_precio)
                                    st.rerun()

                            specs = st.text_input(
                                "Instrucciones (ej. sin cebolla):",
                                value=item_en_carrito.get("especificaciones", ""),
                                key=f"spec_{cat_id}_{pid}"
                            )
                            if specs != item_en_carrito.get("especificaciones", ""):
                                actualizar_especificaciones(pid, specs)

# =========================================================
# COLUMNA DERECHA: CARRITO Y PAGO
# =========================================================
with col_order:
    st.markdown("<h2 style='color:#FFC72C;'>🛒 Tu Carrito</h2>", unsafe_allow_html=True)

    carrito = st.session_state["carrito"]

    if not carrito:
        st.info("Tu carrito está vacío. Elige tus platillos favoritos del menú.")
    else:
        subtotal_orden = sum(d["subtotal"] for d in carrito.values())

        for pid, datos in list(carrito.items()):
            with st.container(border=True):
                c_text, c_del = st.columns([4, 1])
                with c_text:
                    st.markdown(f"**{datos['cantidad']}x {datos['nombre']}**")
                    st.markdown(f"<span style='color:#FFC72C; font-weight:700;'>${datos['subtotal']:.2f}</span>", unsafe_allow_html=True)
                    st.caption(f"📝 {datos['especificaciones']}")
                with c_del:
                    if st.button("❌", key=f"del_cart_{pid}"):
                        del st.session_state["carrito"][pid]
                        st.rerun()

        if st.button("🗑️ Vaciar Carrito", use_container_width=True):
            st.session_state["carrito"] = {}
            st.rerun()

        st.divider()

        # 1. Forma de Entrega
        st.markdown("<h4 style='color:#FFC72C;'>1. Selección de Entrega</h4>", unsafe_allow_html=True)
        modalidad = st.radio(
            "¿Cómo deseas recibir tu pedido?:",
            [f"🛵 Delivery (+${DELIVERY_FEE:.2f})", "🏃 Retiro en Local", "🍽️ Comer en el Food Truck"],
            key="mod_entrega"
        )

        costo_envio = DELIVERY_FEE if "Delivery" in modalidad else 0.0
        if "Delivery" in modalidad:
            direccion_entrega = st.text_area("Dirección exacta con punto de referencia:", key="dir_envio")
        elif "Food Truck" in modalidad:
            direccion_entrega = st.text_input("Número de Mesa:", key="mesa_envio")
        else:
            direccion_entrega = "Retiro directo en local"

        # 2. Forma de Pago
        st.markdown("<h4 style='color:#FFC72C;'>2. Método de Pago</h4>", unsafe_allow_html=True)
        metodo_pago = st.radio("Elige cómo vas a pagar:", ["📱 Pago Móvil (Banesco)", "🟡 Binance Pay", "💵 Efectivo ($ USD)"], key="met_pago")

        referencia_pago = ""
        if "Pago Móvil" in metodo_pago:
            pm = DATOS_PAGO["pago_movil"]
            st.info(f"**Datos Pago Móvil Banesco:**\n- Teléfono: `{pm['telefono']}`\n- Cédula: `{pm['cedula']}`\n- Titular: {pm['titular']}")
            referencia_pago = st.text_input("Número de Referencia / Comprobante:", key="ref_pm")
        elif "Binance" in metodo_pago:
            st.info(f"**Datos Binance Pay:**\nCorreo: `{DATOS_PAGO['binance']['email']}`")
            referencia_pago = st.text_input("ID o Correo de tu cuenta Binance:", key="ref_bn")
        else:
            st.info(DATOS_PAGO['efectivo']['detalle'])
            referencia_pago = st.text_input("¿Con qué billete pagas? (ej. Billete de $20):", key="ref_ef")

        # 3. Datos del Cliente
        st.markdown("<h4 style='color:#FFC72C;'>3. Tu Información</h4>", unsafe_allow_html=True)
        cliente_nombre = st.text_input("Nombre y Apellido:", key="cli_nom")
        cliente_telefono = st.text_input("Teléfono WhatsApp:", key="cli_tel")

        total_final = subtotal_orden + costo_envio

        st.markdown(
            f"""
            <div style="background-color: rgba(20, 20, 25, 0.9); padding: 15px; border-radius: 12px; border: 1px solid #E51B24; margin-top: 15px;">
                <div style="display:flex; justify-content:space-between; color:#AAAAAA; font-size:14px;">
                    <span>Subtotal:</span><span style="color:#FFF;">${subtotal_orden:.2f}</span>
                </div>
                <div style="display:flex; justify-content:space-between; color:#AAAAAA; font-size:14px;">
                    <span>Delivery:</span><span style="color:#FFF;">${costo_envio:.2f}</span>
                </div>
                <hr style="border-color:#333;">
                <div style="display:flex; justify-content:space-between; font-size:20px; font-weight:900; color:#FFC72C;">
                    <span>TOTAL:</span><span>${total_final:.2f}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Validación
        listo = True
        if not cliente_nombre:
            st.warning("⚠️ Por favor escribe tu nombre.")
            listo = False
        elif "Delivery" in modalidad and not direccion_entrega:
            st.warning("⚠️ Por favor indica la dirección para el Delivery.")
            listo = False

        if listo:
            ticket_msg = f"🧾 *PEDIDO — {NOMBRE_NEGOCIO.upper()}*\n"
            ticket_msg += f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %I:%M %p')}\n"
            ticket_msg += f"👤 Cliente: {cliente_nombre}\n"
            ticket_msg += f"📱 Teléfono: {cliente_telefono}\n"
            ticket_msg += f"📍 Modo: {modalidad}\n"
            ticket_msg += f"🏠 Dirección/Mesa: {direccion_entrega}\n"
            ticket_msg += "========================\n"
            for datos in carrito.values():
                ticket_msg += f"• {datos['cantidad']}x {datos['nombre']} (${datos['subtotal']:.2f})\n"
                ticket_msg += f"  Nota: {datos['especificaciones']}\n"
            ticket_msg += "========================\n"
            ticket_msg += f"Subtotal: ${subtotal_orden:.2f}\n"
            if costo_envio > 0:
                ticket_msg += f"Delivery: ${costo_envio:.2f}\n"
            ticket_msg += f"*TOTAL A PAGAR: ${total_final:.2f}*\n"
            ticket_msg += f"💳 Pago: {metodo_pago}\n"
            if referencia_pago:
                ticket_msg += f"Ref/Detalle: {referencia_pago}\n"

            url_wa = f"https://api.whatsapp.com/send?phone={WHATSAPP_PHONE}&text={urllib.parse.quote(ticket_msg)}"

            st.markdown(
                f"""
                <a href="{url_wa}" target="_blank" class="wa-btn">
                    📲 ENVIAR PEDIDO A WHATSAPP
                </a>
                """,
                unsafe_allow_html=True
            )