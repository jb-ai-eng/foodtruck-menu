import os
import urllib.parse
import streamlit as st
from menu_data import (
    NOMBRE_NEGOCIO,
    ESLOGAN,
    INSTAGRAM,
    WHATSAPP_PHONE,
    DELIVERY_FEE,
    DATOS_PAGO,
    CATEGORIAS,
    MENU_ITEMS,
)

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
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Fondo general: Amarillo cálido y vibrante Street Food */
    .stApp {
        background: linear-gradient(135deg, #FFDE59 0%, #FFC107 50%, #FFA000 100%) !important;
        background-attachment: fixed !important;
        color: #1F2937;
    }

    /* Ocultar barra superior y pie por defecto */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Animaciones Clave */
    @keyframes floatLogo {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-8px) rotate(-1deg); }
    }

    @keyframes pulseGlow {
        0%, 100% { transform: scale(1); box-shadow: 0 4px 15px rgba(229, 37, 33, 0.35); }
        50% { transform: scale(1.02); box-shadow: 0 8px 25px rgba(229, 37, 33, 0.6); }
    }

    @keyframes pulseWa {
        0%, 100% { transform: scale(1); box-shadow: 0 6px 20px rgba(37, 211, 102, 0.4); }
        50% { transform: scale(1.03); box-shadow: 0 10px 30px rgba(37, 211, 102, 0.7); }
    }

    @keyframes popBadge {
        0% { transform: scale(0.85); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }

    /* Hero Header Container */
    .hero-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border: 2px solid #FFE082;
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 25px;
        box-shadow: 0 12px 35px rgba(180, 83, 9, 0.18);
        transition: all 0.3s ease;
    }
    .hero-container:hover {
        box-shadow: 0 16px 45px rgba(180, 83, 9, 0.28);
    }

    .hero-logo-img {
        animation: floatLogo 4s ease-in-out infinite;
        filter: drop-shadow(0 8px 15px rgba(0,0,0,0.15));
    }

    .hero-badge-open {
        background: linear-gradient(135deg, #10B981, #059669);
        color: #FFFFFF;
        font-size: 13px;
        font-weight: 700;
        padding: 6px 16px;
        border-radius: 30px;
        display: inline-block;
        margin-bottom: 10px;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
    }

    .hero-title {
        color: #E52521;
        font-size: 34px;
        font-weight: 900;
        margin: 0;
        letter-spacing: -0.5px;
        text-shadow: 1px 1px 0px rgba(0,0,0,0.05);
    }

    .hero-subtitle {
        color: #4B5563;
        font-size: 15px;
        margin-top: 4px;
        font-weight: 500;
    }

    .hero-social-tag {
        display: inline-flex;
        align-items: center;
        background-color: #FFF3CD;
        color: #B45309;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 700;
        text-decoration: none;
        border: 1px solid #FFE082;
        transition: all 0.2s ease;
    }
    .hero-social-tag:hover {
        background-color: #E52521;
        color: #FFFFFF;
        border-color: #E52521;
        transform: translateY(-2px);
    }

    /* Barra Flotante / Destacada del Carrito Activo */
    .cart-alert-bar {
        background: #1F2937;
        color: #FFD000;
        padding: 14px 20px;
        border-radius: 16px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 2px solid #FFD000;
        animation: pulseGlow 3s infinite;
        box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    }

    /* Cards de Productos (Blancas, modernas y súper animadas) */
    .product-card {
        background: #FFFFFF;
        border-radius: 22px;
        border: 2px solid #FFE58F;
        overflow: hidden;
        margin-bottom: 15px;
        box-shadow: 0 10px 25px rgba(180, 83, 9, 0.12);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
    }
    .product-card:hover {
        transform: translateY(-8px) scale(1.015);
        border-color: #E52521;
        box-shadow: 0 18px 40px rgba(229, 37, 33, 0.22);
    }

    .product-img-box {
        position: relative;
        width: 100%;
        height: 160px;
        background: radial-gradient(circle, #FFFBEB 0%, #FDE68A 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        border-bottom: 2px solid #FFE58F;
    }
    .product-emoji {
        font-size: 75px;
        transition: transform 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);
        filter: drop-shadow(0 10px 10px rgba(0,0,0,0.15));
    }
    .product-card:hover .product-emoji {
        transform: scale(1.2) rotate(5deg);
    }

    .product-badge {
        position: absolute;
        top: 12px;
        left: 12px;
        background: linear-gradient(135deg, #E52521, #FF5722);
        color: white;
        padding: 5px 12px;
        border-radius: 14px;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        box-shadow: 0 4px 12px rgba(229, 37, 33, 0.45);
        letter-spacing: 0.5px;
    }

    .cart-active-badge {
        position: absolute;
        top: 12px;
        right: 12px;
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        padding: 5px 12px;
        border-radius: 14px;
        font-size: 12px;
        font-weight: 800;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
        animation: popBadge 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .product-price-tag {
        position: absolute;
        bottom: 12px;
        right: 12px;
        background: rgba(31, 41, 55, 0.92);
        backdrop-filter: blur(6px);
        border: 2px solid #FFC700;
        color: #FFC700;
        padding: 5px 14px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: 900;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }

    .product-info {
        padding: 16px 18px;
    }
    .product-name {
        color: #111827;
        font-size: 19px;
        font-weight: 800;
        margin-bottom: 6px;
    }
    .product-desc {
        color: #4B5563;
        font-size: 13px;
        line-height: 1.5;
        min-height: 48px;
    }

    /* Caja de Pago Informativa en Barra Lateral */
    .payment-info-box {
        background-color: #FFFBEB;
        border: 1px solid #FDE68A;
        border-left: 5px solid #F59E0B;
        padding: 12px 14px;
        border-radius: 10px;
        margin-top: 10px;
        margin-bottom: 15px;
        font-size: 13px;
        color: #92400E;
    }

    /* Botón de WhatsApp Gigante Animado */
    .whatsapp-btn {
        display: block;
        width: 100%;
        background: linear-gradient(135deg, #25D366, #128C7E);
        color: #FFFFFF !important;
        text-align: center;
        padding: 16px 20px;
        font-size: 19px;
        font-weight: 800;
        border-radius: 16px;
        text-decoration: none;
        animation: pulseWa 2.5s infinite;
        transition: all 0.3s ease;
        margin-top: 18px;
    }
    .whatsapp-btn:hover {
        background: linear-gradient(135deg, #2EEB72, #15A392);
        color: #FFFFFF !important;
        transform: scale(1.03);
    }

    /* Resumen de totales */
    .summary-card {
        background: #F9FAFB;
        border: 2px solid #E5E7EB;
        border-radius: 16px;
        padding: 16px;
        margin-top: 15px;
    }
    .summary-line {
        display: flex;
        justify-content: space-between;
        font-size: 14px;
        margin-bottom: 6px;
        color: #4B5563;
        font-weight: 500;
    }
    .summary-total {
        display: flex;
        justify-content: space-between;
        font-size: 20px;
        font-weight: 900;
        color: #E52521;
        border-top: 2px dashed #D1D5DB;
        padding-top: 10px;
        margin-top: 8px;
    }

    /* Pestañas de Streamlit con Estilo Fast Food */
    div[data-baseweb="tab-list"] {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 16px;
        padding: 6px;
        gap: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    }
    div[data-baseweb="tab"] {
        border-radius: 12px !important;
        font-weight: 700 !important;
        color: #4B5563 !important;
        padding: 8px 16px !important;
    }
    div[aria-selected="true"] {
        background-color: #E52521 !important;
        color: #FFFFFF !important;
    }

    /* Sidebar con fondo blanco suave */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 2px solid #FFE082 !important;
        box-shadow: 5px 0 25px rgba(0,0,0,0.08);
    }
    </style>
    """,
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
                    {total_items_carrito} { 'platillo' if total_items_carrito == 1 else 'platillos' }
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

                # Badge visual de si ya está en el carrito
                cart_badge_html = f'<div class="cart-active-badge">✓ {cant_actual} en orden</div>' if cant_actual > 0 else ''

                # Card HTML
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

                # Controles de Cantidad y Personalización
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
                        placeholder="Ej. Sin cebolla, tártara...",
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
        # Desglose de ítems
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

        # -------------------------------------------------
        # MODALIDAD DE ENTREGA
        # -------------------------------------------------
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
                placeholder="Ej. Calle 5 con Av. Principal, Casa #12 (Frente a la panadería)",
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

        # -------------------------------------------------
        # MÉTODO DE PAGO
        # -------------------------------------------------
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
            ref_pago = st.text_input(
                "Número de Referencia (o últimos 4 dígitos):",
                placeholder="Ej. 948210",
                key="ref_pago_movil",
            )
        elif metodo_pago == "🟡 Binance Pay":
            bn = DATOS_PAGO["binance"]
            st.markdown(
                f"""
                <div class="payment-info-box">
                    <b>Correo Binance:</b><br>
                    <code style="color:#B45309; font-weight:700;">{bn['email']}</code><br>
                    <small>Envía captura o ID de pago por WhatsApp.</small>
                </div>
                """,
                unsafe_allow_html=True,
            )
            ref_pago = st.text_input(
                "ID de Transacción / Usuario Binance:",
                placeholder="Ej. Pay ID o tu usuario",
                key="ref_binance",
            )
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
            ref_pago = st.text_input(
                "¿Con cuánto pagas? (Para preparar cambio):",
                placeholder="Ej. Pago con billete de $20 o monto exacto",
                key="ref_efectivo",
            )

        st.markdown("<hr style='border:none; border-top:1px solid #E5E7EB; margin:15px 0;'>", unsafe_allow_html=True)

        # -------------------------------------------------
        # DATOS DEL CLIENTE
        # -------------------------------------------------
        st.markdown("<h4 style='color:#111827; margin-bottom:6px; font-size:15px;'>👤 Tus Datos</h4>", unsafe_allow_html=True)
        cliente_nombre = st.text_input("Tu Nombre Completo:", placeholder="Ej. Carlos Hernández", key="cli_nombre")
        cliente_telefono = st.text_input("Tu Teléfono de Contacto:", placeholder="Ej. 0414-1234567", key="cli_telefono")

        # -------------------------------------------------
        # RESUMEN ECONÓMICO FINAL
        # -------------------------------------------------
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

        # -------------------------------------------------
        # BOTÓN & MENSAJE DE WHATSAPP
        # -------------------------------------------------
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