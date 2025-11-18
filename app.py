import sqlite3
from flask import Flask, request, redirect, session, flash, render_template 
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'clave_secreta'

PRODUCTS = [
    {"id": 1, "name": "Mouse Óptico", "price": 1500, "image": "product1.jpg"},
    {"id": 2, "name": "Teclado Mecánico", "price": 3200, "image": "product2.jpg"},
    {"id": 3, "name": "Auriculares Gamer", "price": 5400, "image": "product3.jpg"}
]

USERS_DB = 'users.db'

def ensure_users_table():
    conn = sqlite3.connect(USERS_DB)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
    conn.commit()
    conn.close()

ensure_users_table()

def get_db_connection():
    conn = sqlite3.connect(USERS_DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template("home.html", username=session.get('username'))

@app.route('/reserva')
def reserva():
    return render_template("reserva.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            return "Completa todos los campos."
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        if cur.fetchone():
            conn.close()
            return "El usuario ya existe."
        hash_pw = generate_password_hash(password)
        cur.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, hash_pw))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        valid_password = False
        if user:
            stored_password = user['password']
            valid_password = stored_password == password or check_password_hash(stored_password, password)

        if user and valid_password:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect('/')
        else:
            flash('Usuario o contrasena incorrectos.')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Cerraste sesion.')
    return redirect('/login')

@app.route('/productos')
def productos():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template("productos.html", products=PRODUCTS)

@app.route('/add/<int:product_id>', methods=['POST'])
def add(product_id):
    qty = int(request.form.get('quantity', 1))
    cart = session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] += qty
    else:
        cart[str(product_id)] = qty
    session['cart'] = cart
    return redirect('/cart')

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect('/login')
    cart_items = []
    total = 0
    for pid, qty in session.get('cart', {}).items():
        product = next((p for p in PRODUCTS if p['id'] == int(pid)), None)
        if product:
            subtotal = product['price'] * qty
            total += subtotal
            cart_items.append({"product": product, "qty": qty, "subtotal": subtotal})
    return render_template("cart.html", items=cart_items, total=total)

@app.route('/checkout')
def checkout():
    session['cart'] = {}
    return render_template("checkout.html")

if __name__ == '__main__':
    app.run(debug=True)
