# 🍔 Victor's Fast Food: Digital Menu

An interactive digital menu for **Victor's Fast Food**, a food truck located in Urbanización Manoa, calle Jiraharas. Customers can browse the menu, customize their order, and send it directly via WhatsApp as a formatted ticket.

🔗 **Live app:** https://foodtruck-menu.streamlit.app
📸 **Instagram:** [@victorsfast_food](https://www.instagram.com/victorsfast_food/)

---

## ✨ Features

- 📋 **Menu by category:** hot dogs, burgers, wraps, specials, sides, and drinks.
- ✏️ **Order customization:** remove ingredients ("no onion", "no tomato"), pick two proteins for the double/mixed burger, and add special notes.
- 🛒 **Shopping cart:** increase or decrease quantities, with the total calculated automatically.
- 🛵 **Delivery or pickup:** delivery adds a $3 fee to the total.
- 💳 **Payment methods:** Pago Móvil and Binance.
- 💬 **WhatsApp ordering:** generates a ticket with all the order details and sends it to the business's number.
- 📱 **Mobile-friendly design.**

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core logic and logo loading |
| Streamlit | Web app deployment |
| HTML and CSS | Menu structure and styling |
| JavaScript | Cart, customization, and ticket generation |
| GitHub | Version control |

## 📁 Project Structure

## 🚀 Run It Locally

1. Clone the repository:
```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
   cd YOUR-REPOSITORY
```
2. Install the dependencies:
```bash
   pip install -r requirements.txt
```
3. Run the app:
```bash
   streamlit run app.py
```

## ⚙️ Configuration

At the top of `app.py` you can change:

- `WHATSAPP`: the number that receives orders, including the country code.
- `DIRECCION`: the business address.
- `DELIVERY_FEE`: the delivery fee.

## 👨‍💻 Author

Built by **Jesús** as part of my learning journey in programming, data analytics, and AI engineering.

- GitHub: [YOUR-USERNAME](https://github.com/YOUR-USERNAME)
