import os
import urllib.parse
import streamlit as st

# ---------------------------------------------------------
# DATOS DEL NEGOCIO & MENÚ COMPLETO
# ---------------------------------------------------------
NOMBRE_NEGOCIO = "Victor's Fast Food"
ESLOGAN = "El auténtico sabor urbano y callejero"
INSTAGRAM = "victorsfast_food"
WHATSAPP_PHONE = "584249367077"
DELIVERY_FEE = 3.00

DATOS_PAGO = {
    "pago_movil": {
        "banco": "Banesco (0134)",
        "telefono": "0424-9367077",
        "cedula": "20.505.294",
        "titular": "Victor"
    },
    "binance": {
        "email": "Hugo_victor_17@hotmail.com",
        "red": "Binance Pay / Correo"
    },
    "efectivo": {
        "moneda": "Dólares ($ USD) en efectivo",
        "detalle": "Tener monto exacto o especificar con cuánto pagará para el vuelto."
    }
}

CATEGORIAS = [
    {"id": "todos", "nombre": "🔥 Todo el Menú", "icono": "🔥"},
    {"id": "hamburguesas", "nombre": "Hamburguesas", "icono": "🍔"},
    {"id": "perros", "nombre": "Perros Calientes", "icono": "🌭"},
    {"id": "pepitos", "nombre": "Pepitos y Enrollados", "icono": "🌯"},
    {"id": "especiales", "nombre": "Sandwiches & Salchipapa", "icono": "🥪"},
    {"id": "extras", "nombre": "Raciones & Tequeños", "icono": "🍟"},
    {"id": "bebidas", "nombre": "Bebidas", "icono": "🥤"},
]

MENU_ITEMS = [
    {"id": "hamb_sencilla", "categoria": "hamburguesas", "nombre": "Hamburguesa Sencilla", "precio": 6.00, "descripcion": "Pan suave, carne jugosa a la plancha, lechuga, tomate fresco, cebolla, papitas ralladas y queso amarillo.", "badge": "Clásica", "foto": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=700&q=80"},
    {"id": "hamb_carne", "categoria": "hamburguesas", "nombre": "Hamburguesa de Carne", "precio": 8.00, "descripcion": "Pan artesanal, carne premium, tocineta crujiente, jamón, queso americano, huevo frito, lechuga, tomate, cebolla y papitas.", "badge": "Favorita 🔥", "foto": "https://images.unsplash.com/photo-1586190848861-99aa4a171e90?auto=format&fit=crop&w=700&q=80"},
    {"id": "hamb_pollo", "categoria": "hamburguesas", "nombre": "Hamburguesa de Pollo", "precio": 8.00, "descripcion": "Pan, pechuga de pollo marinada a la plancha, tocineta, jamón, queso americano, huevo, lechuga, tomate, cebolla y papitas.", "badge": "Top Ventas", "foto": "https://images.unsplash.com/photo-1606755962773-d324e0a13086?auto=format&fit=crop&w=700&q=80"},
    {"id": "hamb_chuleta", "categoria": "hamburguesas", "nombre": "Hamburguesa de Chuleta", "precio": 8.00, "descripcion": "Pan, chuleta ahumada a la plancha con sabor único, tocineta, jamón, queso americano, huevo, vegetales y lluvia de papitas.", "badge": "Especialidad 🥩", "foto": "https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=700&q=80"},
    {"id": "hamb_crispy", "categoria": "hamburguesas", "nombre": "Hamburguesa Crispy", "precio": 9.00, "descripcion": "Pollo frito extra empanizado super crujiente, lechuga fresca, tomate, cebolla, tocineta, jamón, queso amarillo y papitas fritas.", "badge": "Mega Crispy 🍗", "foto": "https://images.unsplash.com/photo-1625813506062-0aeb1d7a094b?auto=format&fit=crop&w=700&q=80"},
    {"id": "hamb_doble_mixta", "categoria": "hamburguesas", "nombre": "Hamburguesa Doble o Mixta", "precio": 15.00, "descripcion": "¡Poder total! Pan gigante, dos proteínas de tu preferencia (carne, pollo o chuleta), tocineta, jamón, queso americano, huevo frito, vegetales y papitas.", "badge": "La Gigante 👑", "foto": "https://images.unsplash.com/photo-1583032015879-c55675f920f2?auto=format&fit=crop&w=700&q=80"},
    {"id": "perro_pequeno", "categoria": "perros", "nombre": "Perro Pequeño", "precio": 2.50, "descripcion": "Pan suave pequeño, salchicha nacional de primera, lechuga, tomate, cebolla picadita, queso amarillo rallado, papitas crocantes y salsas.", "badge": "Económico 🌭", "foto": "https://images.unsplash.com/photo-1619740455993-9e612b1af08a?auto=format&fit=crop&w=700&q=80"},
    {"id": "perro_sencillo", "categoria": "perros", "nombre": "Perro Sencillo (Grande)", "precio": 3.50, "descripcion": "Pan grande, salchicha nacional, repollo/lechuga, cebolla, tomate, lluvia de papitas ralladas doradas, queso amarillo y salsas de la casa.", "badge": "El Callejero 🛞", "foto": "https://images.unsplash.com/photo-1627308595229-7830a5c91f9f?auto=format&fit=crop&w=700&q=80"},
    {"id": "perro_especial", "categoria": "perros", "nombre": "Perro Especial con Todo", "precio": 5.00, "descripcion": "Pan grande, salchicha nacional, jamón a la plancha, tocineta crujiente, huevo, queso amarillo rallado abundante, papitas y todas las salsas.", "badge": "Más Pedido ⭐", "foto": "https://images.unsplash.com/photo-1612392062422-ef19b42f74df?auto=format&fit=crop&w=700&q=80"},
    {"id": "perro_polaco", "categoria": "perros", "nombre": "Perro Polaco Supremo", "precio": 8.00, "descripcion": "Pan grande, salchicha polaca ahumada y sazonada, tocineta, jamón, huevo, queso amarillo, papitas crocantes y salsas al gusto.", "badge": "Polaco Premium", "foto": "https://images.unsplash.com/photo-1541214113241-21578d2d9b62?auto=format&fit=crop&w=700&q=80"},
    {"id": "pepito_mixto", "categoria": "pepitos", "nombre": "Pepito Mixto Especial", "precio": 25.00, "descripcion": "El rey de la noche: Pan de pepito relleno de carne tierna y pollo a la plancha, jamón, queso fundido, tocineta, huevo frito, vegetales, papitas y baño de salsas.", "badge": "Super Cargado 💥", "foto": "https://images.unsplash.com/photo-1509722747041-616f39b57569?auto=format&fit=crop&w=700&q=80"},
    {"id": "mini_pepito", "categoria": "pepitos", "nombre": "Mini Pepito", "precio": 10.00, "descripcion": "Para un antojo perfecto: Carne jugosa, vegetales frescos, tocineta, queso amarillo derretido y lluvia de papitas.", "badge": "Rápido & Sabroso", "foto": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=700&q=80"},
    {"id": "enrollado_mixto", "categoria": "pepitos", "nombre": "Enrollado Mixto", "precio": 20.00, "descripcion": "Tortilla suave enrollada con abundante carne y pollo a la plancha, jamón, queso, tocineta, huevo, lechuga, tomate, cebolla y papitas.", "badge": "Estilo Shawarma 🌯", "foto": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?auto=format&fit=crop&w=700&q=80"},
    {"id": "enrollado_carne", "categoria": "pepitos", "nombre": "Enrollado de Carne", "precio": 20.00, "descripcion": "Enrollado con carne sazonada, jamón, queso, tocineta, lechuga, tomate, cebolla, papitas y huevo.", "badge": "Pura Carne", "foto": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?auto=format&fit=crop&w=700&q=80"},
    {"id": "enrollado_pollo", "categoria": "pepitos", "nombre": "Enrollado de Pollo", "precio": 20.00, "descripcion": "Enrollado con pechuga de pollo en tiras bien sazonada, jamón, queso, tocineta, huevo, vegetales y papitas crocantes.", "badge": "Pollo Tierno", "foto": "https://images.unsplash.com/photo-1529006557810-274b9b2fc783?auto=format&fit=crop&w=700&q=80"},
    {"id": "salchipapa", "categoria": "especiales", "nombre": "Salchipapa Victor's", "precio": 15.00, "descripcion": "Enorme bandeja de papas fritas doradas, trozos abundantes de salchicha parrillera, tocineta crujiente, queso fundido y salsas especiales.", "badge": "Para Compartir 🍟", "foto": "https://images.unsplash.com/photo-1585109649139-366815a0d713?auto=format&fit=crop&w=700&q=80"},
    {"id": "club_house", "categoria": "especiales", "nombre": "Sandwich Club House", "precio": 12.00, "descripcion": "4 pisos triangulares con pechuga de pollo desmechada/plancha, jamón, queso amarillo, huevo, lechuga, tomate, cebolla y servido con papas fritas.", "badge": "Clásico Americano 🥪", "foto": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=700&q=80"},
    {"id": "sandwich_granjero", "categoria": "especiales", "nombre": "Sandwich Granjero", "precio": 9.00, "descripcion": "Pan suave campesino/granjero, pechuga de pollo, lechuga, tomate, cebolla, queso amarillo derretido y papitas fritas crocantes.", "badge": "Delicioso", "foto": "https://images.unsplash.com/photo-1553909489-cd47e0907980?auto=format&fit=crop&w=700&q=80"},
    {"id": "tequenos", "categoria": "extras", "nombre": "Ración de Tequeños (6 uds)", "precio": 6.00, "descripcion": "Dorado perfecto y masa crujiente, rellenos de auténtico queso blanco venezolano derretido. Acompañados de salsa tártara de la casa.", "badge": "Indispensable 🧀", "foto": "https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?auto=format&fit=crop&w=700&q=80"},
    {"id": "papa_500", "categoria": "extras", "nombre": "Ración de Papas Fritas (500 gr)", "precio": 5.00, "descripcion": "Medio kilo de papas fritas bien doradas y crujientes con su toque de sal y salsas.", "badge": "500 Gramos", "foto": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=700&q=80"},
    {"id": "papa_250", "categoria": "extras", "nombre": "Ración de Papas Fritas (250 gr)", "precio": 2.50, "descripcion": "250 gramos de papas fritas recién hechas, crocantes y listas para acompañar tu comida.", "badge": "250 Gramos", "foto": "https://images.unsplash.com/photo-1576107232684-1279f3908594?auto=format&fit=crop&w=700&q=80"},
    {"id": "nestea", "categoria": "bebidas", "nombre": "Nestea Helado de Limón", "precio": 2.00, "descripcion": "Vaso de Nestea con abundante hielo, cítrico, dulce y refrescante. El match perfecto de la comida rápida.", "badge": "El Favorito 🍋", "foto": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=700&q=80"},
    {"id": "refresco_botella", "categoria": "bebidas", "nombre": "Refresco Botellita (355ml)", "precio": 1.50, "descripcion": "Coca-Cola, Pepsi, Chinotto o Hit helado en botella individual para acompañar tu orden.", "badge": "Fría 🧊", "foto": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=700&q=80"},
    {"id": "refresco_1l", "categoria": "bebidas", "nombre": "Refresco 1.0 Litro Familiar", "precio": 3.00, "descripcion": "Botella de 1 Litro bien fría para compartir entre amigos o familia.", "badge": "Para Compartir", "foto": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?auto=format&fit=crop&w=700&q=80"},
]

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title=f"{NOMBRE_NEGOCIO} | Menú & Pedidos Online",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# 2. ESTILOS CSS PERSONALIZADOS
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    .stApp { background-color: #0E0F12; color: #F3F4F6; }
    header {visibility: hidden;}
    footer {visibility: hidden;}

    .hero-badge-open {
        background-color: #10B981; color: #FFFFFF; font-size: 13px; font-weight: 700;
        padding: 5px 14px; border-radius: 20px; display: inline-block; margin-bottom: 12px;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.4);
    }
    .hero-social-tag {
        display: inline-flex; align-items: center; background-color: #222530; color: #FFC700;
        padding: 6px 14px; border-radius: 30px; font-size: 14px; font-weight: 600;
        text-decoration: none; border: 1px solid #323644;
    }
    .product-card {
        background-color: #161820; border: 1px solid #262936; border-radius: 16px;
        overflow: hidden; margin-bottom: 20px; transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .product-card:hover { transform: translateY(-3px); border-color: #FFC700; }
    .product-img-box { position: relative; width: 100%; height: 180px; overflow: hidden; }
    .product-img { width: 100%; height: 100%; object-fit: cover; }
    .product-badge {
        position: absolute; top: 12px; left: 12px;
        background: linear-gradient(135deg, #E52521, #FF5722); color: white;
        padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 700; text-transform: uppercase;
    }
    .product-price-tag {
        position: absolute; bottom: 12px; right: 12px; background-color: rgba(14, 15, 18, 0.88);
        border: 1px solid #FFC700; color: #FFC700; padding: 4px 12px; border-radius: 10px;
        font-size: 17px; font-weight: 800;
    }
    .product-info { padding: 16px; }
    .product-name { color: #FFFFFF; font-size: 18px; font-weight: 700; margin-bottom: 6px; }
    .product-desc { color: #9CA3AF; font-size: 13px; line-height: 1.5; min-height: 48px; }
    .payment-info-box {
        background-color: #161821; border-left: 4px solid #FFC700; padding: 14px 16px;
        border-radius: 10px; margin-top: 10px; margin-bottom: 15px; font-size: 14px; color: #E2E8F0;
    }
    .whatsapp-btn {
        display: block; width: 100%; background: linear-gradient(135deg, #25D366, #128C7E);
        color: #FFFFFF !important; text-align: center; padding: 16px 20px; font-size: 19px;
        font-weight: 800; border-radius: 14px; text-decoration: none;
        box-shadow: 0 6px 20px rgba(37, 211, 102, 0.4); margin-top: 15px;
    }
    .whatsapp-btn:hover { background: linear-gradient(135deg, #2EEB72, #15A392); color: #FFFFFF !important; }
    .summary-card { background: #14161D; border: 1px solid #282B37; border-radius: 14px; padding: 18px; margin-top: 15px; }
    .summary-line { display: flex; justify-content: space-between; font-size: 15px; margin-bottom: 8px; color: #D1D5DB; }
    .summary-total {
        display: flex; justify-content: space-between; font-size: 20px; font-weight: 800;
        color: #FFC700; border-top: 1px solid #374151; padding-top: 10px; margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 3. GESTIÓN DEL ESTADO
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
# 4. HERO HEADER
# ---------------------------------------------------------
logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

col_logo, col_info = st.columns([1, 4])
with col_logo:
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.title("🍔")

with col_info:
    st.markdown(
        f"""
        <div style="padding-top: 5px;">
            <div class="hero-badge-open">🟢 ABIERTO AHORA • TOMANDO PEDIDOS</div>
            <h1 style="color:#FFC700; margin:0; font-size:34px; font-weight:900;">{NOMBRE_NEGOCIO}</h1>
            <p style="color:#A0A5B5; margin:4px 0 10px 0; font-size:15px;">{ESLOGAN}</p>
            <div>
                <a class="hero-social-tag" href="https://instagram.com/{INSTAGRAM}" target="_blank">
                    📸 Instagram: @{INSTAGRAM}
                </a>
                <span style="color:#A0A5B5; font-size:13px; margin-left:12px;">
                    🛵 Delivery disponible (+${DELIVERY_FEE:.2f}) | 🏃 Pick-Up / En Mesa
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border:none; border-top:1px solid #222530; margin:20px 0;'>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. MENÚ POR CATEGORÍAS
# ---------------------------------------------------------
nombres_tabs = [cat["nombre"] for cat in CATEGORIAS]
tabs = st.tabs(nombres_tabs)

for i, tab in enumerate(tabs):
    cat_id = CATEGORIAS[i]["id"]
    with tab:
        items_a_mostrar = MENU_ITEMS if cat_id == "todos" else [item for item in MENU_ITEMS if item["categoria"] == cat_id]
        col_left, col_right = st.columns(2)
        for idx, item in enumerate(items_a_mostrar):
            col_target = col_left if idx % 2 == 0 else col_right
            with col_target:
                item_id = item["id"]
                nombre = item["nombre"]
                precio = item["precio"]
                desc = item["descripcion"]
                badge = item["badge"]
                foto = item["foto"]

                item_en_carrito = st.session_state["carrito"].get(item_id, {})
                cant_actual = item_en_carrito.get("cantidad", 0)
                notas_actual = item_en_carrito.get("notas", "")

                st.markdown(
                    f"""
                    <div class="product-card">
                        <div class="product-img-box">
                            <img src="{foto}" class="product-img" alt="{nombre}">
                            <div class="product-badge">{badge}</div>
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
                    cant = st.number_input("Cantidad:", min_value=0, max_value=20, value=cant_actual, step=1, key=f"qty_{cat_id}_{item_id}")
                with c_notes:
                    notas = st.text_input("Personalizar:", value=notas_actual, placeholder="Ej. Sin cebolla...", key=f"notes_{cat_id}_{item_id}")

                if cant != cant_actual or notas != notas_actual:
                    actualizar_carrito(item_id, nombre, precio, cant, notas)
                    st.rerun()

                st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. CHECKOUT & CARRITO
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""<div style="text-align:center; padding:10px 0;"><h2 style="color:#FFC700; margin:0; font-size:24px;">🛒 Tu Pedido</h2></div>""", unsafe_allow_html=True)
    carrito = st.session_state["carrito"]

    if not carrito:
        st.markdown("""<div style="text-align:center; padding: 40px 10px; color:#6B7280;"><div style="font-size:48px;">🛍️</div><p>Tu carrito está vacío</p></div>""", unsafe_allow_html=True)
    else:
        subtotal_comida = 0.0
        for item_id, datos in list(carrito.items()):
            subtotal_comida += datos["subtotal"]
            st.markdown(
                f"""
                <div style="background:#14161E; border:1px solid #232634; border-radius:10px; padding:10px 12px; margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:700; color:#FFFFFF; font-size:14px;">{datos['cantidad']}x {datos['nombre']}</span>
                        <span style="color:#FFC700; font-weight:800; font-size:14px;">${datos['subtotal']:.2f}</span>
                    </div>
                    {f'<div style="color:#94A3B8; font-size:11px; margin-top:3px; font-style:italic;">📝 {datos["notas"]}</div>' if datos['notas'] else ''}
                </div>
                """,
                unsafe_allow_html=True,
            )

        if st.button("🗑️ Vaciar Carrito", use_container_width=True):
            st.session_state["carrito"] = {}
            st.rerun()

        st.markdown("<h4 style='color:#FFFFFF; margin-bottom:8px; font-size:16px;'>📍 Tipo de Entrega</h4>", unsafe_allow_html=True)
        modalidad = st.radio("Selecciona modalidad:", [f"🛵 Delivery a domicilio (+${DELIVERY_FEE:.2f})", "🏃 Para Llevar (Pick-Up)", "🍽️ Comer en el Local / Mesa"], key="tipo_entrega")
        costo_delivery = DELIVERY_FEE if "Delivery" in modalidad else 0.0
        detalle_entrega = st.text_area("🏠 Dirección de Entrega:", key="dir_delivery") if "Delivery" in modalidad else (st.text_input("Número de Mesa:", key="num_mesa") if "Local" in modalidad else "Retiro en Local")

        st.markdown("<h4 style='color:#FFFFFF; margin-bottom:8px; font-size:16px;'>💳 Método de Pago</h4>", unsafe_allow_html=True)
        metodo_pago = st.radio("¿Cómo vas a pagar?", ["📱 Pago Móvil", "🟡 Binance Pay", "💵 Efectivo ($ USD)"], key="metodo_pago")

        ref_pago = ""
        if metodo_pago == "📱 Pago Móvil":
            pm = DATOS_PAGO["pago_movil"]
            st.markdown(f"""<div class="payment-info-box"><b>Banco:</b> {pm['banco']}<br><b>Teléfono:</b> <code style="color:#FFC700;">{pm['telefono']}</code><br><b>Cédula:</b> <code style="color:#FFC700;">{pm['cedula']}</code><br><b>Titular:</b> {pm['titular']}</div>""", unsafe_allow_html=True)
            ref_pago = st.text_input("Referencia:", key="ref_pago_movil")
        elif metodo_pago == "🟡 Binance Pay":
            bn = DATOS_PAGO["binance"]
            st.markdown(f"""<div class="payment-info-box"><b>Correo Binance:</b><br><code style="color:#FFC700;">{bn['email']}</code></div>""", unsafe_allow_html=True)
            ref_pago = st.text_input("Usuario o ID Binance:", key="ref_binance")
        else:
            st.markdown(f"""<div class="payment-info-box"><b>Efectivo ($ USD):</b><br>{DATOS_PAGO['efectivo']['detalle']}</div>""", unsafe_allow_html=True)
            ref_pago = st.text_input("¿Con cuánto pagas?:", key="ref_efectivo")

        st.markdown("<h4 style='color:#FFFFFF; margin-bottom:8px; font-size:16px;'>👤 Tus Datos</h4>", unsafe_allow_html=True)
        cliente_nombre = st.text_input("Tu Nombre Completo:", key="cli_nombre")
        cliente_telefono = st.text_input("Tu Teléfono:", key="cli_telefono")

        total_pagar = subtotal_comida + costo_delivery
        st.markdown(f"""<div class="summary-card"><div class="summary-line"><span>Subtotal:</span><span>${subtotal_comida:.2f}</span></div><div class="summary-line"><span>Delivery:</span><span>+${costo_delivery:.2f}</span></div><div class="summary-total"><span>TOTAL:</span><span>${total_pagar:.2f}</span></div></div>""", unsafe_allow_html=True)

        if not cliente_nombre:
            st.warning("⚠️ Ingresa tu nombre para ordenar.")
        elif "Delivery" in modalidad and not detalle_entrega:
            st.warning("⚠️ Ingresa tu dirección de entrega.")
        elif "Local" in modalidad and not detalle_entrega:
            st.warning("⚠️ Ingresa el número de mesa.")
        else:
            msg = f"🔥 *NUEVO PEDIDO - {NOMBRE_NEGOCIO}* 🔥\n"
            msg += "--------------------------------------\n"
            msg += f"👤 *Cliente:* {cliente_nombre}\n"
            if cliente_telefono: msg += f"📱 *Teléfono:* {cliente_telefono}\n"
            msg += f"📍 *Modalidad:* {modalidad}\n"
            if detalle_entrega: msg += f"🏠 *Detalle:* {detalle_entrega}\n"
            msg += "--------------------------------------\n📋 *DETALLE:*\n"
            for item_id, datos in carrito.items():
                msg += f"• *{datos['cantidad']}x* {datos['nombre']} — ${datos['subtotal']:.2f}\n"
                if datos["notas"]: msg += f"   ↳ _Nota: {datos['notas']}_\n"
            msg += "--------------------------------------\n"
            msg += f"🍔 *Subtotal:* ${subtotal_comida:.2f}\n"
            if costo_delivery > 0: msg += f"🛵 *Delivery:* ${costo_delivery:.2f}\n"
            msg += f"💰 *TOTAL A PAGAR:* *${total_pagar:.2f}*\n"
            msg += f"💳 *Pago:* {metodo_pago}\n"
            if ref_pago: msg += f"🔢 *Referencia:* {ref_pago}\n"
            msg += "--------------------------------------\n¡Hola! Acabo de armar mi pedido. ¿Me confirman la orden por favor? 🙏"

            url_wa = f"https://wa.me/{WHATSAPP_PHONE}?text={urllib.parse.quote(msg)}"
            st.markdown(f"""<a href="{url_wa}" target="_blank" class="whatsapp-btn">📲 Enviar Pedido por WhatsApp</a>""", unsafe_allow_html=True)