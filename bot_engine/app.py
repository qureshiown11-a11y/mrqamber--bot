from flask import Flask, request, jsonify
import sqlite3
from flask import render_template_string,session) 
app = Flask(__name__)
app.secret_key = 'abc123'
# Database banane wala function
def init_db():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS restaurants
                 (id INTEGER PRIMARY KEY, name TEXT, whatsapp_number TEXT, status TEXT)''')
    # Dough Joe demo data
    c.execute("INSERT OR IGNORE INTO restaurants VALUES (1, 'Dough Joe', '92300XXXXXXX', 'ON')")
    conn.commit()
    conn.close()

init_db()
@app.route('/admin')
def admin():
    status = 'ON'
    return f'<h1>Bot Status: {status}</h1><button>OFF</button>'
    
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    phone = data.get('from', '92300XXXXXXX')
    msg = data.get('message', '').lower()
    to_number = data.get('to', '92300XXXXXXX')

    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("SELECT name,status FROM restaurants WHERE whatsapp_number=?", (to_number,))
    restaurant = c.fetchone()
    conn.close()

    if not restaurant:
        return jsonify({"reply": "Restaurant not found bhai"})

    # KILL SWITCH CHECK
    if restaurant[1] == 'OFF':
        return jsonify({"reply": "Bot temporarily closed. Contact MR_QAMBER for renewal"})

    # Bot reply logic
    if 'menu' in msg or 'hi' in msg or 'hello' in msg:
        reply = f"Salam! {restaurant[0]} me khush aamdeed 🍕\n1. Malai Boti Fiesta Large - Rs 2840\n2. Smokey Chicken Medium - Rs 1990\nOrder ke liye naam + size likho\nPowered by MR_QAMBER"
    elif 'large' in msg or 'medium' in msg:
        reply = f"Zabardast! {msg} order le liya ✅\nAddress + Phone number bhejo delivery ke liye"
    else:
        reply = "Bhai 'Menu' likho, phir item select karo. Asaan hai 😄"

    return jsonify({"reply": reply})

@app.route("/")
def home():
    return "MR_QAMBER Bot Engine LIVE 🔥 Kill Switch Ready!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
