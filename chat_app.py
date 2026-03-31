from flask import Flask, render_template, request
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__, template_folder='chat_templates')
app.config['SECRET_KEY'] = 'kenny-chat-secret'
socketio = SocketIO(app)

users = {}

@app.route('/')
def home():
    return render_template('chat.html')

@socketio.on('connect')
def handle_connect():
    print(f'User connected: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        username = users[request.sid]
        del users[request.sid]
        emit('message', {
            'user': 'System',
            'text': f'{username} left the chat',
            'time': datetime.now().strftime('%H:%M'),
            'type': 'system'
        }, broadcast=True)

@socketio.on('join')
def handle_join(data):
    username = data['username']
    users[request.sid] = username
    emit('message', {
        'user': 'System',
        'text': f'{username} joined the chat!',
        'time': datetime.now().strftime('%H:%M'),
        'type': 'system'
    }, broadcast=True)
    emit('online_count', {'count': len(users)}, broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    emit('message', {
        'user': data['username'],
        'text': data['text'],
        'time': datetime.now().strftime('%H:%M'),
        'type': 'user'
    }, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5004)