from flask import Flask, render_template, request, redirect, session
from db_config import get_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        gmail = request.form['gmail']
        phone = request.form['phone']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, gmail, phone, password) VALUES (%s, %s, %s, %s)",
                       (username, gmail, phone, password))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    trains = [
        {'name': 'Express 101', 'id': 1},
        {'name': 'FastTrack', 'id': 2},
        {'name': 'Night Rider', 'id': 3},
        {'name': 'Sunrise Special', 'id': 4},
    ]
    return render_template('dashboard.html', trains=trains)

@app.route('/book/<int:train_id>', methods=['GET', 'POST'])
def book_ticket(train_id):
    if request.method == 'POST':
        cls = request.form['class']
        people = int(request.form['people'])
        username = session['username']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO tickets (username, train_id, class, people)
                          VALUES (%s, %s, %s, %s)""", (username, train_id, cls, people))
        conn.commit()
        conn.close()
        return render_template('ticket_success.html', train_id=train_id, cls=cls, people=people)
    return render_template('book_ticket.html', train_id=train_id)

@app.route('/my_tickets')
def my_tickets():
    username = session['username']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tickets WHERE username=%s", (username,))
    tickets = cursor.fetchall()
    conn.close()
    return render_template('my_tickets.html', tickets=tickets)

if __name__ == '__main__':
    app.run(debug=True)
