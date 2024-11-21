import socket
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    Paitent = data['username']
    Sigil = data['room']
    join_room(Sigil)
    send(f'{Paitent} has entered the Sigil.', to=Sigil)

@socketio.on('leave')
def on_leave(data):
    Paitent = data['username']
    Sigil = data['room']
    leave_room(Sigil)
    send(f'{Paitent} has left the Sigil.', to=Sigil)

@socketio.on('message')
def handle_message(data):
    Sigil = data['room']
    send(data['message'], to=Sigil)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to an external IP address to get the local IP address
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    host_ip = get_local_ip()
    print(f"Running on IP: {host_ip}")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
