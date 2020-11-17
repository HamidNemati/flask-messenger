from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app)

# creating databse and table if users
db = sqlite3.connect('messenger.db',check_same_thread=False)
db.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, fname TEXT NOT NULL, lname TEXT NOT NULL)')

def query_db(query, args=(), one=False):
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def welcome():
    
    return render_template('Start.html')


@app.route('/server')
def Server():
    return render_template('Server.html')




@app.route('/username')
def Username(methods=['GET', 'POST']):
    return render_template('Username.html')


@app.route('/username check')
def CheckUsername(methods=['GET', 'POST']):
    
    first_name = request.args.get('fname')
    last_name = request.args.get('lname')
    name_exist = query_db('select * from users where fname=? and lname=?',[first_name, last_name], one=True)
    print(name_exist)
    
    if (name_exist == None):
         query_db('INSERT INTO users(fname, lname) VALUES(?, ?)', args=[first_name, last_name])
         return render_template('session.html')
    else:
         duplicate=True
         return render_template('Username.html', duplicate = duplicate)
         
         





@app.route('/chatroom')
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
 