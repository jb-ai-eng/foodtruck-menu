import base64
import pathlib

import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# CONFIGURACIÓN DEL NEGOCIO
# ==========================================
WHATSAPP = "584249367077"
DIRECCION = "Urbanización Manoa, calle Jiraharas"
DELIVERY_FEE = 3

st.set_page_config(page_title="Victor's Fast Food", page_icon="🍔", layout="centered")

st.markdown(
    """<style>
    #MainMenu, header, footer {visibility: hidden;}
    .block-container {padding-top: 0.5rem; padding-bottom: 0; max-width: 720px;}
    </style>""",
    unsafe_allow_html=True,
)

base = pathlib.Path(__file__).parent
logo_file = next((base / n for n in ["logo.png", "logo.jpg", "logo.jpeg"] if (base / n).exists()), None)
if logo_file:
    mime = "png" if logo_file.suffix == ".png" else "jpeg"
    logo_b64 = base64.b64encode(logo_file.read_bytes()).decode()
    logo_html = f'<div class="logo"><img src="data:image/{mime};base64,{logo_b64}" alt="Logo"></div>'
else:
    logo_html = "<h1>🍔 Victor's Fast Food</h1>"

HTML = r"""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{--bg:#FFF9EC;--card:#FFFFFF;--soft:#FFF1C9;--acc:#D9342B;--acc2:#F5D33B;--txt:#1F1F1F;--mut:#6B6B6B;--line:#F0E3C4;--dark:#111111}
*{box-sizing:border-box}
body{margin:0;font-family:Poppins,sans-serif;background:var(--bg);color:var(--txt)}
.wrap{max-width:680px;margin:0 auto;padding:12px 12px 40px}
.hero{background:var(--dark);border-radius:20px;padding:16px 16px 18px;text-align:center}
.logo{max-width:260px;margin:0 auto 6px}
.logo img{width:100%;height:auto;display:block}
h1{margin:0 0 6px;font-size:22px;color:var(--acc2)}
.sub{margin:4px 0 0;font-size:13px;color:#E8E8E8}
.cats{display:flex;gap:8px;overflow-x:auto;padding:14px 0 10px}
.chip{border:1px solid var(--line);background:#fff;border-radius:999px;padding:8px 14px;font:inherit;font-size:14px;white-space:nowrap;cursor:pointer;color:var(--txt)}
.chip.on{background:var(--acc);border-color:var(--acc);color:#fff}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px;margin-bottom:10px}
.row{display:flex;gap:12px;align-items:flex-start}
.emo{font-size:28px;width:48px;height:48px;border-radius:12px;background:var(--soft);display:flex;align-items:center;justify-content:center;flex:none}
.name{margin:0;font-weight:600;font-size:15px}
.desc{margin:3px 0 0;font-size:12.5px;color:var(--mut);line-height:1.5}
.price{font-weight:600;color:var(--acc);font-size:16px;white-space:nowrap}
.btn{border:1px solid var(--line);background:#fff;border-radius:10px;padding:8px 12px;font:inherit;font-size:13px;cursor:pointer;color:var(--txt)}
.btn.add{background:var(--acc);border-color:var(--acc);color:#fff;margin-top:6px}
.opt{background:var(--soft);border-radius:12px;padding:12px;margin-top:12px}
.lbl{display:block;font-size:13px;color:var(--mut);margin:12px 0 4px}
input[type=text],select{width:100%;border:1px solid var(--line);border-radius:10px;padding:10px;font:inherit;font-size:14px;background:#fff;color:var(--txt)}
.ck{display:inline-flex;align-items:center;gap:5px;font-size:13px;margin:4px 12px 4px 0}
.seg{display:flex;gap:8px}.seg .btn{flex:1;padding:11px}
.seg .btn.on{background:var(--acc2);border-color:var(--acc2);font-weight:600}
.line{display:flex;align-items:center;gap:8px;padding:10px 0;border-bottom:1px dashed var(--line)}
.q{width:30px;height:30px;padding:0;border-radius:50%}
.tot{display:flex;justify-content:space-between;font-size:14px;color:var(--mut);margin-top:4px}
.big{font-size:20px;font-weight:600;color:var(--txt)}
.send{width:100%;background:#25D366;border:none;color:#fff;border-radius:14px;padding:14px;font:inherit;font-weight:600;font-size:16px;margin-top:10px;cursor:pointer}
.err{color:#C0392B;font-size:13px;margin:8px 0 0;min-height:1em}
.bar{position:sticky;bottom:10px;background:var(--txt);color:#fff;border-radius:14px;padding:13px 16px;display:none;justify-content:space-between;cursor:pointer;margin-top:10px;font-weight:500}
.pay{background:var(--soft);border-radius:12px;padding:12px;font-size:13px;line-height:1.7;margin-top:10px}
pre{white-space:pre-wrap;font-size:12px;margin:0;font-family:inherit}
a.wa{display:block;text-align:center;margin-top:10px;color:#1a9e4b;font-weight:600}
</style>

<div class="wrap">
  <div class="hero">
    __LOGO__
    <div>
      <p class="sub"><a href="https://www.instagram.com/victorsfast_food/" target="_blank" style="color:var(--acc2);font-weight:600;text-decoration:none">📸 @victorsfast_food</a></p>
      <p class="sub">📍 __DIR__</p>
      <p class="sub">🛵 Delivery $__FEE__</p>
    </div>
  </div>

  <div class="cats" id="cats"></div>
  <div id="list"></div>
  <div class="bar" id="bar" onclick="document.getElementById('cartbox').scrollIntoView({behavior:'smooth'})"></div>

  <div class="card" id="cartbox" style="margin-top:16px">
    <p class="name" style="font-size:18px">🛒 Tu pedido</p>
    <div id="cart"></div>

    <span class="lbl">Tipo de entrega</span>
    <div class="seg">
      <button class="btn on" id="m_d" onclick="setMode('d')">🛵 Delivery +$__FEE__</button>
      <button class="btn" id="m_r" onclick="setMode('r')">🏪 Retiro en local</button>
    </div>

    <span class="lbl">👤 Tu nombre</span>
    <input type="text" id="f_n" placeholder="María Pérez" oninput="clr()">
    <span class="lbl">📞 Tu teléfono</span>
    <input type="text" id="f_t" placeholder="0414 1234567" oninput="clr()">
    <div id="adwrap">
      <span class="lbl">📍 Dirección de entrega</span>
      <input type="text" id="f_a" placeholder="Calle, casa, punto de referencia" oninput="clr()">
    </div>

    <span class="lbl">💳 Método de pago</span>
    <div class="seg">
      <button class="btn" id="p_pm" onclick="setPay('pm')">📱 Pago móvil</button>
      <button class="btn" id="p_bn" onclick="setPay('bn')">🪙 Binance</button>
    </div>
    <div id="payinfo"></div>

    <div id="tot" style="margin-top:14px"></div>
    <p class="err" id="err"></p>
    <button class="send" onclick="send()">💬 Enviar pedido por WhatsApp</button>
    <div id="prev"></div>
  </div>
</div>

<script>
const WA = "__WA__";
const FEE = Number("__FEE__");
const CATS = [["Todos","📋"],["Perros","🌭"],["Hamburguesas","🍔"],["Enrollados","🌯"],["Especiales","🥪"],["Extras","🍟"],["Bebidas","🥤"]];
const EMO = {Perros:"🌭",Hamburguesas:"🍔",Enrollados:"🌯",Especiales:"🥪",Extras:"🍟",Bebidas:"🥤"};
const M = [
["Perro Pequeño",2.5,"Pan pequeño, salchicha nacional, lechuga, tomate, cebolla, queso amarillo, papitas y salsa","Perros"],
["Perro Sencillo",3.5,"Pan grande, salchicha nacional, lechuga, tomate, cebolla, queso amarillo, papitas y salsa","Perros"],
["Perro Especial",5,"Pan grande, salchicha nacional, lechuga, tomate, cebolla, jamón, queso amarillo, tocineta y huevo","Perros"],
["Perro Polaco",8,"Pan grande, salchicha polaca, lechuga, tomate, cebolla, jamón, queso amarillo, tocineta y huevo","Perros"],
["Hamburguesa Sencilla",6,"Pan, carne, lechuga, tomate, cebolla, papitas, queso amarillo","Hamburguesas"],
["Hamburguesa de Carne",8,"Pan, carne, lechuga, tomate, cebolla, papitas, tocineta, jamón, queso americano y huevo","Hamburguesas"],
["Hamburguesa de Pollo",8,"Pan, pollo pechuga, lechuga, tomate, cebolla, papitas, tocineta, jamón, queso americano y huevo","Hamburguesas"],
["Hamburguesa Chuleta",8,"Pan, chuleta ahumada, lechuga, tomate, cebolla, papitas, tocineta, jamón, queso americano y huevo","Hamburguesas"],
["Hamburguesa Doble o Mixta",15,"Pan, dos proteínas de preferencia, lechuga, tomate, cebolla, papitas, tocineta, jamón, queso americano y huevo","Hamburguesas"],
["Hamburguesa Crispy",null,"Pollo frito empanizado, lechuga, tomate, cebolla, tocineta, jamón, queso amarillo y papitas fritas","Hamburguesas"],
["Enrollado Carne",20,"Carne, jamón, queso, tocineta, lechuga, tomate, cebolla, papitas y huevo","Enrollados"],
["Enrollado Pollo",20,"Pollo, jamón, queso, tocineta, huevo, lechuga, tomate, cebolla y papitas","Enrollados"],
["Enrollado Mixto",20,"Carne y pollo, jamón, queso, tocineta, huevo, lechuga, tomate, cebolla y papitas","Enrollados"],
["Pepito Mixto",25,"Carne y pollo, jamón, queso, tocineta, huevo, lechuga, tomate, cebolla y papitas","Enrollados"],
["Mini Pepito",10,"Carne, vegetales, papita, tocineta y queso amarillo","Enrollados"],
["Salchipapa",15,"","Especiales"],
["Sandwich Granjero",null,"Pan tipo granjero, lechuga, tomate, cebolla, pollo, queso amarillo y papitas fritas","Especiales"],
["Club House",12,"Pollo, lechuga, tomate, cebolla, jamón, huevo, queso amarillo y papas fritas","Especiales"],
["Ración Papa 500gr",5,"","Extras"],
["Ración Papa 250gr",2.5,"","Extras"],
["Ración Tequeños",null,"","Extras"],
["Nestea",2,"","Bebidas"],
["Refresco Botellita",1,"","Bebidas"],
["Refresco 1.0L",2,"","Bebidas"]
];
const RM = ["lechuga","tomate","cebolla","salsa","papitas","huevo","tocineta","jamón","queso","vegetales"];
let cat = "Todos", open = null, cart = [], mode = "d", pay = "";

const money = n => n == null ? "Consultar" : "$" + n.toFixed(2);
const custom = i => M[i][2] && ["Perros","Hamburguesas","Enrollados","Especiales"].includes(M[i][3]);
const $ = id => document.getElementById(id);

function rCats(){
  $("cats").innerHTML = CATS.map(c => `<button class="chip ${c[0]==cat?"on":""}" onclick="setCat('${c[0]}')">${c[1]} ${c[0]}</button>`).join("");
}
function setCat(c){ cat = c; open = null; rCats(); rList(); }

function rList(){
  let h = "";
  M.forEach((m, i) => {
    if (cat != "Todos" && m[3] != cat) return;
    h += `<div class="card"><div class="row">
      <div class="emo">${EMO[m[3]]}</div>
      <div style="flex:1;min-width:0"><p class="name">${m[0]}</p>${m[2] ? `<p class="desc">${m[2]}</p>` : ""}</div>
      <div style="text-align:right"><div class="price">${money(m[1])}</div>
      <button class="btn add" onclick="tap(${i})">➕ Agregar</button></div></div>`;
    if (open === i){
      const d = m[2].toLowerCase();
      const opts = RM.filter(r => d.includes(r));
      h += `<div class="opt"><p class="name" style="font-size:14px">✨ ¿Cómo lo quieres?</p>`;
      if (m[0].includes("Doble")) h += `<span class="lbl">🥩 Elige tus 2 proteínas</span><div class="seg">
        <select id="p1"><option>Carne</option><option>Pollo</option><option>Chuleta</option></select>
        <select id="p2"><option>Carne</option><option selected>Pollo</option><option>Chuleta</option></select></div>`;
      if (opts.length) h += `<span class="lbl">❌ Quitar ingredientes</span>` + opts.map(o => `<label class="ck"><input type="checkbox" class="sx" value="${o}"> Sin ${o}</label>`).join("");
      h += `<span class="lbl">📝 Nota especial</span><input type="text" id="nt" placeholder="Bien tostado, salsa aparte...">
        <div class="seg" style="margin-top:10px"><button class="btn" onclick="open=null;rList()">Cancelar</button>
        <button class="btn add" style="margin-top:0" onclick="add(${i})">Añadir al carrito</button></div></div>`;
    }
    h += `</div>`;
  });
  $("list").innerHTML = h;
}

function tap(i){ if (custom(i)){ open = open === i ? null : i; rList(); } else add(i); }

function add(i){
  let sin = [], prot = null, note = "";
  if (open === i){
    sin = [...document.querySelectorAll(".sx:checked")].map(x => x.value);
    if ($("p1")) prot = $("p1").value + " + " + $("p2").value;
    note = $("nt").value.trim();
  }
  const key = JSON.stringify([i, sin, prot, note]);
  const ex = cart.find(c => c.k == key);
  if (ex) ex.q++; else cart.push({k:key, i, q:1, sin, prot, note});
  open = null; rList(); rCart(); clr();
}

function qty(n, d){ cart[n].q += d; if (cart[n].q < 1) cart.splice(n, 1); rCart(); }
const sub = () => cart.reduce((s, c) => s + (M[c.i][1] || 0) * c.q, 0);

function rCart(){
  const count = cart.reduce((s, c) => s + c.q, 0);
  const s = sub(), fee = mode == "d" && cart.length ? FEE : 0;
  $("bar").style.display = count ? "flex" : "none";
  $("bar").innerHTML = `<span>🛒 Ver carrito (${count})</span><span>$${(s + fee).toFixed(2)}</span>`;
  $("cart").innerHTML = !cart.length ? `<p class="desc">Agrega algo rico del menú para empezar 😋</p>` :
    cart.map((c, n) => {
      const m = M[c.i];
      const det = [c.prot ? "Proteínas: " + c.prot : "", ...c.sin.map(x => "Sin " + x), c.note ? "Nota: " + c.note : ""].filter(Boolean).join(" · ");
      return `<div class="line"><div style="flex:1;min-width:0"><p class="name" style="font-size:14px">${EMO[m[3]]} ${m[0]}</p>${det ? `<p class="desc">${det}</p>` : ""}</div>
        <button class="btn q" onclick="qty(${n},-1)">−</button><b>${c.q}</b><button class="btn q" onclick="qty(${n},1)">+</button>
        <span style="min-width:64px;text-align:right">${m[1] == null ? "Consultar" : "$" + (m[1] * c.q).toFixed(2)}</span></div>`;
    }).join("");
  const pend = cart.some(c => M[c.i][1] == null);
  $("tot").innerHTML = `<div class="tot"><span>Subtotal</span><span>$${s.toFixed(2)}</span></div>
    <div class="tot"><span>Delivery</span><span>$${fee.toFixed(2)}</span></div>
    <div class="tot big"><span>Total</span><span>$${(s + fee).toFixed(2)}</span></div>
    ${pend ? `<p class="desc">⚠️ Algunos productos tienen precio por confirmar.</p>` : ""}`;
}

function setMode(m){
  mode = m;
  $("m_d").className = "btn" + (m == "d" ? " on" : "");
  $("m_r").className = "btn" + (m == "r" ? " on" : "");
  $("adwrap").style.display = m == "d" ? "block" : "none";
  rCart(); clr();
}

function setPay(p){
  pay = p;
  $("p_pm").className = "btn" + (p == "pm" ? " on" : "");
  $("p_bn").className = "btn" + (p == "bn" ? " on" : "");
  $("payinfo").innerHTML = p == "pm"
    ? `<div class="pay"><b>📱 Pago móvil · Banesco</b><br>Teléfono: 04249367077<br>Cédula: 20505294</div>`
    : `<div class="pay"><b>🪙 Binance</b><br>Hugo_victor_17@hotmail.com</div>`;
  clr();
}

function clr(){ $("err").textContent = ""; }

function send(){
  const n = $("f_n").value.trim(), t = $("f_t").value.trim(), a = $("f_a").value.trim(), e = $("err");
  if (!cart.length) return e.textContent = "Agrega al menos un producto.";
  if (!n) return e.textContent = "Escribe tu nombre.";
  if (!t) return e.textContent = "Escribe tu teléfono.";
  if (mode == "d" && !a) return e.textContent = "Escribe la dirección de entrega.";
  if (!pay) return e.textContent = "Elige un método de pago.";

  const id = Math.floor(1000 + Math.random() * 9000), s = sub(), fee = mode == "d" ? FEE : 0;
  const L = [
    "🍔 *VICTOR'S FAST FOOD* 🌭",
    "🧾 *Pedido #" + id + "*",
    "━━━━━━━━━━━━━━",
    "👤 *Cliente:* " + n,
    "📞 *Teléfono:* " + t,
    mode == "d" ? "🛵 *Entrega:* Delivery\n📍 *Dirección:* " + a : "🏪 *Entrega:* Retiro en el local",
    "━━━━━━━━━━━━━━"
  ];
  cart.forEach(c => {
    const m = M[c.i];
    L.push(EMO[m[3]] + " *" + c.q + "x " + m[0] + "* — " + (m[1] == null ? "Precio a consultar" : "$" + (m[1] * c.q).toFixed(2)));
    if (c.prot) L.push("   🥩 Proteínas: " + c.prot);
    c.sin.forEach(x => L.push("   ❌ Sin " + x));
    if (c.note) L.push("   📝 " + c.note);
  });
  L.push("━━━━━━━━━━━━━━", "💵 Subtotal: $" + s.toFixed(2), "🛵 Delivery: $" + fee.toFixed(2), "💰 *TOTAL: $" + (s + fee).toFixed(2) + "*");
  if (cart.some(c => M[c.i][1] == null)) L.push("⚠️ Incluye productos con precio por confirmar");
  L.push("━━━━━━━━━━━━━━",
    pay == "pm" ? "💳 *Pago:* Pago móvil Banesco\n04249367077 · CI 20505294" : "💳 *Pago:* Binance\nHugo_victor_17@hotmail.com",
    "📸 Enviaré el comprobante de pago por aquí.");

  const msg = L.join("\n");
  const url = "https://wa.me/" + WA + "?text=" + encodeURIComponent(msg);
  $("prev").innerHTML = `<div class="pay"><b>🧾 Tu ticket</b><pre>${msg.replace(/</g, "&lt;")}</pre></div>
    <a class="wa" href="${url}" target="_blank">Si WhatsApp no se abrió, toca aquí 💬</a>`;
  if (WA.includes("X")) return e.textContent = "Falta configurar el número de WhatsApp del local.";
  window.open(url, "_blank");
}

rCats(); rList(); rCart();
</script>
"""

html = (
    HTML.replace("__WA__", WHATSAPP)
    .replace("__DIR__", DIRECCION)
    .replace("__FEE__", str(DELIVERY_FEE))
    .replace("__LOGO__", logo_html)
)

components.html(html, height=2600, scrolling=True)