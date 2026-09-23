import os
import urllib.parse
import streamlit as st

# =========================================================
# DATOS DEL NEGOCIO Y MENÚ (SISTEMA INDEPENDIENTE)
# =========================================================
NOMBRE_NEGOCIO = "🔥 Victor's Fast Food"
ESLOGAN = "Las mejores hamburguesas y comida rápida de la ciudad"
INSTAGRAM = "victorsfastfood"
WHATSAPP_PHONE = "13051234567"  # Cambiar por el número real con código de país
DELIVERY_FEE = 3.00

DATOS_PAGO = {
    "pago_movil": {
        "banco": "Banesco",
        "telefono": "0414-1234567",
        "cedula": "V-12345678",
        "titular": "Victor Fast Food C.A."
    },
    "binance": {
        "email": "pagos@victorsfastfood.com"
    },
    "efectivo": {
        "detalle": "Aceptamos billetes de $ USD en buen estado. Ten el cambio exacto si es posible."
    }
}

CATEGORIAS = [
    {"id": "todos", "nombre": "🍔 Todos"},
    {"id": "hamburguesas", "nombre": "🍔 Hamburguesas"},
    {"id": "perros", "nombre": "🌭 Perros Calientes"},
    {"id": "entradas", "nombre": "🍟 Entradas y Acompañantes"},
    {"id": "bebidas", "nombre": "🥤 Bebidas"},
]

MENU_ITEMS = [
    {
        "id": "hamb_clasica",
        "categoria": "hamburguesas",
        "nombre": "Hamburguesa Clásica",
        "precio": 8.50,
        "descripcion": "Carne de res 150g, queso cheddar, lechuga, tomate y salsa de la casa.",
        "badge": "⭐ Popular",
        "emoji": "🍔"
    },
    {
        "id": "hamb_especial",
        "categoria": "hamburguesas",
        "nombre": "Super Victor Burger",
        "precio": 12.00,
        "descripcion": "Doble carne, doble tocino, queso fundido, cebolla caramelizada y huevo frito.",
        "badge": "🔥 Recomendado",
        "emoji": "🍔"
    },
    {
        "id": "dog_clasico",
        "categoria": "perros",
        "nombre": "Hot Dog Tradicional",
        "precio": 5.00,
        "descripcion": "Salchicha premium, papitas ralladas, cebolla y trío de salsas.",
        "badge": "Clásico",
        "emoji": "🌭"
    },
    {
        "id": "dog_especial",
        "categoria": "perros",
        "nombre": "Perro Caliente Especial",
        "precio": 7.50,
        "descripcion": "Con tocino crujiente, queso derretido, maíz y salsa tártara.",
        "badge": "💥 Favorito",
        "emoji": "🌭"
    },
    {
        "id": "papas_simples",
        "categoria": "entradas",
        "nombre": "Papas Fritas Crujientes",
        "precio": 4.00,
        "descripcion": "Papas sazonadas con sal marina y servidas con salsa de ajo.",
        "badge": "Acompañante",
        "emoji": "🍟"
    },
    {
        "id": "refresco",
        "categoria": "bebidas",
        "nombre": "Soda / Refresco 355ml",
        "precio": 2.00,
        "descripcion": "Lata fría (Coca-Cola, Sprite, Fanta).",
        "badge": "Frío",
        "emoji": "🥤"
    }
]

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title=f"{NOMBRE_NEGOCIO} | Menú Digital & Pedidos",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# 2. ESTILOS CSS PERSONALIZADOS (FONDO AMARILLO ANIMADO & CARDS BLANCAS)
# ---------------------------------------------------------
st.markdown(
    
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 3. GESTIÓN DEL ESTADO (CARRITO)
# ---------------------------------------------------------
if "carrito" not in st.session_state:
    st.session_state["carrito"] = {}

def actualizar_carrito(item_id, item_nombre, item_precio, cantidad, notas):
    if cantidad > 0:
        st.session_state["carrito"][item_id] = {
            "nombre": item_nombre,
            "precio": item_precio,
            "cantidad": cantidad,
            "subtotal": cantidad * item_precio,
            "notas": notas.strip() if notas else "",
        }
    else:
        if item_id in st.session_state["carrito"]:
            del st.session_state["carrito"][item_id]

# ---------------------------------------------------------
# 4. HERO HEADER CON LOGO OFICIAL
# ---------------------------------------------------------
logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

with st.container():
    col_logo, col_info = st.columns([1, 4])
    with col_logo:
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
        else:
            st.markdown("<div style='font-size:64px; text-align:center;'>🍔</div>", unsafe_allow_html=True)

    with col_info:
        st.markdown(
            f"""
            <div style="padding-top: 5px;">
                <div class="hero-badge-open">🟢 ABIERTO • TOMANDO PEDIDOS</div>
                <h1 class="hero-title">{NOMBRE_NEGOCIO}</h1>
                <p class="hero-subtitle">{ESLOGAN}</p>
                <div style="margin-top: 8px;">
                    <a class="hero-social-tag" href="https://instagram.com/{INSTAGRAM}" target="_blank">
                        📸 Instagram: @{INSTAGRAM}
                    </a>
                    <span style="color:#6B7280; font-size:13px; font-weight:600; margin-left:12px;">
                        🛵 Delivery directo (+${DELIVERY_FEE:.2f}) | 🏃 Pick-Up / Mesa
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Barra de estado si hay ítems en el carrito
total_items_carrito = sum(d["cantidad"] for d in st.session_state["carrito"].values())
total_subtotal_carrito = sum(d["subtotal"] for d in st.session_state["carrito"].values())

if total_items_carrito > 0:
    st.markdown(
        f"""
        <div class="cart-alert-bar">
            <div>
                <span style="font-size:20px;">🛒</span> 
                <b style="color:#FFFFFF; font-size:16px;">Tu Carrito:</b> 
                <span style="background:#E52521; color:#fff; font-weight:800; padding:2px 8px; border-radius:10px; margin:0 5px;">
                    {total_items_carrito} {'platillo' if total_items_carrito == 1 else 'platillos'}
                </span>
                <span style="color:#FFD000; font-weight:800; font-size:16px;">${total_subtotal_carrito:.2f}</span>
            </div>
            <div style="font-size:13px; font-weight:700; color:#FFFFFF;">
                👉 Revisa y envía en la barra lateral
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. PESTAÑAS DEL MENÚ POR CATEGORÍAS
# ---------------------------------------------------------
nombres_tabs = [cat["nombre"] for cat in CATEGORIAS]
tabs = st.tabs(nombres_tabs)

for i, tab in enumerate(tabs):
    cat_id = CATEGORIAS[i]["id"]
    with tab:
        if cat_id == "todos":
            items_a_mostrar = MENU_ITEMS
        else:
            items_a_mostrar = [item for item in MENU_ITEMS if item["categoria"] == cat_id]

        col_left, col_right = st.columns(2)
        for idx, item in enumerate(items_a_mostrar):
            col_target = col_left if idx % 2 == 0 else col_right

            with col_target:
                item_id = item["id"]
                nombre = item["nombre"]
                precio = item["precio"]
                desc = item["descripcion"]
                badge = item["badge"]
                emoji = item.get("emoji", "🍔")

                item_en_carrito = st.session_state["carrito"].get(item_id, {})
                cant_actual = item_en_carrito.get("cantidad", 0)
                notas_actual = item_en_carrito.get("notas", "")

                cart_badge_html = f'<div class="cart-active-badge">✓ {cant_actual} en orden</div>' if cant_actual > 0 else ''

                st.markdown(
                    f"""
                    <div class="product-card">
                        <div class="product-img-box">
                            <div class="product-emoji">{emoji}</div>
                            <div class="product-badge">{badge}</div>
                            {cart_badge_html}
                            <div class="product-price-tag">${precio:.2f}</div>
                        </div>
                        <div class="product-info">
                            <div class="product-name">{nombre}</div>
                            <div class="product-desc">{desc}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                c_qty, c_notes = st.columns([1, 2])
                with c_qty:
                    cant = st.number_input(
                        "Cantidad:",
                        min_value=0,
                        max_value=20,
                        value=cant_actual,
                        step=1,
                        key=f"qty_{cat_id}_{item_id}",
                    )
                with c_notes:
                    notas = st.text_input(
                        "Personalizar:",
                        value=notas_actual,
                        placeholder="Ej. Sin cebolla...",
                        key=f"notes_{cat_id}_{item_id}",
                    )

                if cant != cant_actual or notas != notas_actual:
                    actualizar_carrito(item_id, nombre, precio, cant, notas)
                    st.rerun()

                st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. BARRA LATERAL (CHECKOUT & CARRITO DE COMPRAS)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding:10px 0;">
            <div style="font-size:36px;">🛒</div>
            <h2 style="color:#E52521; margin:0; font-size:24px; font-weight:900;">Tu Pedido</h2>
            <p style="color:#6B7280; font-size:13px; margin:2px 0 0 0;">Revisa tus platillos y confirma</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='border:none; border-top:2px dashed #E5E7EB; margin:12px 0;'>", unsafe_allow_html=True)

    carrito = st.session_state["carrito"]

    if not carrito:
        st.markdown(
            """
            <div style="text-align:center; padding: 40px 10px; color:#9CA3AF;">
                <div style="font-size:48px;">🍔🌭🍟</div>
                <p style="margin-top:12px; font-weight:700; font-size:15px; color:#374151;">¡Tu carrito está vacío!</p>
                <p style="font-size:13px;">Elige tus platillos favoritos en el menú para armar tu orden.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        subtotal_comida = 0.0
        for item_id, datos in list(carrito.items()):
            subtotal_comida += datos["subtotal"]
            st.markdown(
                f"""
                <div style="background:#F9FAFB; border:1px solid #E5E7EB; border-radius:12px; padding:10px 12px; margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:700; color:#111827; font-size:14px;">{datos['cantidad']}x {datos['nombre']}</span>
                        <span style="color:#E52521; font-weight:800; font-size:14px;">${datos['subtotal']:.2f}</span>
                    </div>
                    {f'<div style="color:#6B7280; font-size:11px; margin-top:3px; font-style:italic;">📝 {datos["notas"]}</div>' if datos['notas'] else ''}
                </div>
                """,
                unsafe_allow_html=True,
            )

        if st.button("🗑️ Vaciar Carrito", use_container_width=True):
            st.session_state["carrito"] = {}
            st.rerun()

        st.markdown("<hr style='border:none; border-top:1px solid #E5E7EB; margin:15px 0;'>", unsafe_allow_html=True)

        st.markdown("<h4 style='color:#111827; margin-bottom:6px; font-size:15px;'>📍 Tipo de Entrega</h4>", unsafe_allow_html=True)
        modalidad = st.radio(
            "Selecciona cómo recibirás tu orden:",
            [
                f"🛵 Delivery a domicilio (+${DELIVERY_FEE:.2f})",
                "🏃 Para Llevar (Pick-Up)",
                "🍽️ Comer en el Local / Mesa",
            ],
            key="tipo_entrega",
        )

        costo_delivery = 0.0
        detalle_entrega = ""

        if "Delivery" in modalidad:
            costo_delivery = DELIVERY_FEE
            detalle_entrega = st.text_area(
                "🏠 Dirección exacta y Punto de Referencia:",
                placeholder="Ej. Calle 5 con Av. Principal, Casa #12",
                key="dir_delivery",
            )
        elif "Local" in modalidad:
            detalle_entrega = st.text_input(
                "Número de Mesa:",
                placeholder="Ej. Mesa 4",
                key="num_mesa",
            )
        else:
            detalle_entrega = "Retiro en Food Truck (Para Llevar)"

        st.markdown("<hr style='border:none; border-top:1px solid #E5E7EB; margin:15px 0;'>", unsafe_allow_html=True)

        st.markdown("<h4 style='color:#111827; margin-bottom:6px; font-size:15px;'>💳 Método de Pago</h4>", unsafe_allow_html=True)
        metodo_pago = st.radio(
            "¿Cómo vas a pagar?",
            ["📱 Pago Móvil", "🟡 Binance Pay", "💵 Efectivo ($ USD)"],
            key="metodo_pago",
        )

        ref_pago = ""
        if metodo_pago == "📱 Pago Móvil":
            pm = DATOS_PAGO["pago_movil"]
            st.markdown(
                f"""
                <div class="payment-info-box">
                    <b>Banco:</b> {pm['banco']}<br>
                    <b>Teléfono:</b> <code style="color:#B45309; font-weight:700;">{pm['telefono']}</code><br>
                    <b>Cédula:</b> <code style="color:#B45309; font-weight:700;">{pm['cedula']}</code><br>
                    <b>Titular:</b> {pm['titular']}
                </div>
                """,
                unsafe_allow_html=True,
            )
            ref_pago = st.text_input("Número de Referencia:", placeholder="Ej. 948210", key="ref_pago_movil")
        elif metodo_pago == "🟡 Binance Pay":
            bn = DATOS_PAGO["binance"]
            st.markdown(
                f"""
                <div class="payment-info-box">
                    <b>Correo Binance:</b><br>
                    <code style="color:#B45309; font-weight:700;">{bn['email']}</code>
                </div>
                """,
                unsafe_allow_html=True,
            )
            ref_pago = st.text_input("ID de Transacción / Binance:", placeholder="Ej. Pay ID", key="ref_binance")
        else:
            st.markdown(
                f"""
                <div class="payment-info-box">
                    <b>Efectivo ($ USD):</b><br>
                    {DATOS_PAGO['efectivo']['detalle']}
                </div>
                """,
                unsafe_allow_html=True,
            )
            ref_pago = st.text_input("¿Con cuánto pagas?:", placeholder="Ej. Billete de $20", key="ref_efectivo")

        st.markdown("<hr style='border:none; border-top:1px solid #E5E7EB; margin:15px 0;'>", unsafe_allow_html=True)

        st.markdown("<h4 style='color:#111827; margin-bottom:6px; font-size:15px;'>👤 Tus Datos</h4>", unsafe_allow_html=True)
        cliente_nombre = st.text_input("Tu Nombre Completo:", placeholder="Ej. Carlos Hernández", key="cli_nombre")
        cliente_telefono = st.text_input("Tu Teléfono de Contacto:", placeholder="Ej. 0414-1234567", key="cli_telefono")

        total_pagar = subtotal_comida + costo_delivery

        st.markdown(
            f"""
            <div class="summary-card">
                <div class="summary-line">
                    <span>Subtotal Platillos:</span>
                    <span>${subtotal_comida:.2f}</span>
                </div>
                <div class="summary-line">
                    <span>Costo Delivery:</span>
                    <span>{f"+${costo_delivery:.2f}" if costo_delivery > 0 else "Gratis ($0.00)"}</span>
                </div>
                <div class="summary-total">
                    <span>TOTAL A PAGAR:</span>
                    <span>${total_pagar:.2f}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        puede_enviar = True
        error_msg = ""

        if not cliente_nombre:
            puede_enviar = False
            error_msg = "Por favor indica tu nombre."
        elif "Delivery" in modalidad and not detalle_entrega:
            puede_enviar = False
            error_msg = "Por favor indica tu dirección de entrega."
        elif "Local" in modalidad and not detalle_entrega:
            puede_enviar = False
            error_msg = "Por favor indica tu número de mesa."

        if not puede_enviar:
            st.warning(f"⚠️ {error_msg}")
        else:
            msg = f"🔥 *NUEVO PEDIDO - {NOMBRE_NEGOCIO}* 🔥\n"
            msg += "--------------------------------------\n"
            msg += f"👤 *Cliente:* {cliente_nombre}\n"
            if cliente_telefono:
                msg += f"📱 *Teléfono:* {cliente_telefono}\n"
            msg += f"📍 *Modalidad:* {modalidad}\n"
            if detalle_entrega:
                msg += f"🏠 *Detalle Entrega:* {detalle_entrega}\n"
            msg += "--------------------------------------\n"
            msg += "📋 *DETALLE DEL PEDIDO:*\n"

            for item_id, datos in carrito.items():
                msg += f"• *{datos['cantidad']}x* {datos['nombre']} — ${datos['subtotal']:.2f}\n"
                if datos["notas"]:
                    msg += f"   ↳ _Nota: {datos['notas']}_\n"

            msg += "--------------------------------------\n"
            msg += f"🍔 *Subtotal Comida:* ${subtotal_comida:.2f}\n"
            if costo_delivery > 0:
                msg += f"🛵 *Delivery Fee:* ${costo_delivery:.2f}\n"
            msg += f"💰 *TOTAL A PAGAR:* *${total_pagar:.2f}*\n"
            msg += "--------------------------------------\n"
            msg += f"💳 *Método de Pago:* {metodo_pago}\n"
            if ref_pago:
                msg += f"🔢 *Detalle/Ref de Pago:* {ref_pago}\n"
            msg += "--------------------------------------\n"
            msg += "¡Hola! Acabo de armar mi pedido por el menú web. ¿Me confirman la orden por favor? 🙏"

            url_whatsapp = f"https://wa.me/{WHATSAPP_PHONE}?text={urllib.parse.quote(msg)}"

            st.markdown(
                f"""
                <a href="{url_whatsapp}" target="_blank" class="whatsapp-btn">
                    📲 Enviar Pedido por WhatsApp
                </a>
                <p style="text-align:center; color:#6B7280; font-size:11px; margin-top:8px;">
                    Al tocar se abrirá WhatsApp con el pedido listo para enviar.
                </p>
                """,
                unsafe_allow_html=True,
            )