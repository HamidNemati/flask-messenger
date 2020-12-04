from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app)


clients = []

# creating databse and tables 
db = sqlite3.connect('messenger.db',check_same_thread=False)
db.execute('DROP TABLE IF EXISTS users')
db.execute('DROP TABLE IF EXISTS groups')
db.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,socketid TEXT NOT NULL, fname TEXT NOT NULL, lname TEXT NOT NULL)')
db.execute('CREATE TABLE IF NOT EXISTS groups(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)')

room = 'general'

def query_db(query, args=(), one=False):
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def welcome():
    
    if (query_db('select * from groups where name = ?',args=["general"],one=True) is None):
        query_db('insert into groups(name) values(?)',args=["general"])
        print('a group made')
    return render_template('Start.html')


@app.route('/server')
def Server():
    return render_template('Server.html',db = db)




@app.route('/username')
def Username(methods=['GET', 'POST']):
    return render_template('Username.html')


@app.route('/username check')
def CheckUsername(methods=['GET', 'POST']):
    
    print(request.args.get('new group'))
    first_name = request.args.get('fname')
    last_name = request.args.get('lname')
    name_exist = query_db('select * from users where fname=? and lname=?',[first_name, last_name], one=True)
    print(name_exist)
    
    if (name_exist is None):
         return render_template('session.html',fname = first_name , lname = last_name, room = room )
    else:
         duplicate=True
         return render_template('Username.html', duplicate = duplicate)
         
         





@app.route('/chatroom')
def sessions():
    
    return render_template('session.html')



def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')



@app.route('/new_group')
def new_group(methods=['GET', 'POST']):
    return render_template('new group.html')





@socketio.on('my event')
def handle_my_custom_event(json, methodes=['GET', 'POST']):
    
    name = (json.get('user_name'))
    id = str(json.get('id'))
    
    if (id not in clients and id is not None and name is not None):
        print('new user : {} '.format(name))
        first_name, last_name = name.split()
        clients.append(id)
        query_db('INSERT INTO users(socketid, fname, lname) VALUES(?, ?, ?)', args=[id, first_name, last_name])
        join_room(room = room)

    
    print('received my event: ' + str(json))
    if (json.get('data') is not None):
        json.update({'user_name':name+' joined ...'})
        json.update({'message':''})
        socketio.emit('my response', json, callback=messageReceived , broadcast=True)
    else:
        socketio.emit('my response', json, callback=messageReceived , room = room)






@socketio.on('disconnect')
def test_disconnect(methodes=['GET', 'POST']):
    if (request.sid in clients):
        
        clients.remove(request.sid)
        client = query_db('SELECT * FROM users WHERE socketid=?', args=[request.sid])
        name = client[0][2]+" "+client[0][3]+" has left..."
        json = {'user_name':name , 'message':''}
        socketio.emit('my response', json, callback=messageReceived , broadcast=True)
        query_db('DELETE FROM users WHERE socketid=?',args=[request.sid])
        print('{} is disconnected'.format(request.sid))



if __name__ == '__main__':
    socketio.run(app, debug=True)
 