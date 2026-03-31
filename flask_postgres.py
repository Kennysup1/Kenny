from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host="localhost",
        database="kennydb",
        user="postgres",
        password="kenny123",
        port="5432"
    )

@app.route('/')
def home():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY id")
    users = cursor.fetchall()
    conn.close()
    return jsonify([{
        'id': u[0],
        'name': u[1],
        'email': u[2],
        'age': u[3]
    } for u in users])

@app.route('/user/<name>')
def get_user(name):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({'id': user[0], 'name': user[1], 'email': user[2], 'age': user[3]})
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5003)