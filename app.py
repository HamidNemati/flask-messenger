from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def welcome():
    return render_template('Start.html')


@app.route('/server')
def Server():
    return render_template('Server.html')


@app.route('/username')
def Username(methods=['GET', 'POST']):
    print(request.args.get('fname') ,request.args.get('lname'))
    return render_template('Username.html')





@app.route('/chatroom/')
def sessions():
    return render_template('session.html')



def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methodes=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)
 