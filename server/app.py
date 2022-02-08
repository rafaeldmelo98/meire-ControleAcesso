import sqlite3
from flask import Flask, request

app = Flask(__name__)

conn = sqlite3.connect('database.db')
conn.execute('''CREATE TABLE IF NOT EXISTS users (user TEXT, password TEXT, key_user TEXT)''')
conn.execute('''CREATE TABLE IF NOT EXISTS booking_request (num_request TEXT, key_user TEXT, 
date_request TEXT, accepted INTEGER, start_time_request TEXT, end_time_request TEXT)''')
conn.close()


# Rotas
@app.route('/')
def home():
    return {'msg': 'Página inicial'}


@app.route('/teste', methods=['POST'])
def teste():
    if request.method == 'POST':
        json = request.json
        return {'recebido':json}


@app.route('/login', methods=['POST'])
def login():
    con = sqlite3.connect("database.db")
    try:
        data = request.json
        user = data['user']
        password = data['password']
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE user=?", (user,))
        user_db = cur.fetchone()
        if user_db[1] == password:
            msg = 'User logged.'
            login = True
        else:
            msg = 'User or password incorrect.'
            login = False
    except Exception as e:
        con.rollback()
        msg = f"Error trying to log user. Error: {e}"
        login = False
    finally:
        con.close()
        return {
            'user': user_db,
            'msg': msg,
            'login': login}, 201


@app.route('/register', methods=['POST'])
def register():
    con = sqlite3.connect("database.db")
    try:
        data = request.json
        user = data['user']
        password = data['password']
        key_user = data['key']
        json = request.json
        print(json)

        cur = con.cursor()
        cur.execute("INSERT INTO users(user, password, key_user) \
            VALUES(?, ?, ?)", (user, password, key_user))
        con.commit()
        msg = 'User created!'
    except Exception as e:
        con.rollback()
        msg = f"Error while. Error: {e}"
    finally:
        con.close()
        return {'msg': msg}


@app.route('/booking', methods=['GET','POST'])
def booking():
    con = sqlite3.connect("database.db")
    if request.method == 'POST':
        try:
            data = request.json
            key_user = data['key']
            data_request = data['data_request']
            start_time_request = data['start_time_request']
            end_time_request = data['end_time_request']
            cur = con.cursor()
            cur.execute('SELECT COUNT(*) FROM booking_request')
            id = cur.fetchone()
            id = str((int(id[0])+1))
            cur.execute('INSERT INTO booking_request(num_request, key_user, date_request, \
            start_time_request, end_time_request,accepted) VALUES (?,?,?,?,?,0)', 
            (id,key_user,data_request,start_time_request,end_time_request))
            print('Erro3')
            con.commit()
            msg = 'Date booked!'
        except Exception as e:
            con.rollback()
            msg = f"Error while. Error: {e}"
        finally:
            con.close()
            return {'msg': msg}
    if request.method == 'GET':
        try:
            data = request.json
            num_request = data['num_request']
            cur = con.cursor()
            cur.execute("SELECT * FROM booking_request WHERE num_request=?", (num_request,))
            booking_request = cur.fetchone()
            if booking_request:
                msg = 'Request found'
            else:
                msg = 'Request not found'
        except Exception as e:
            msg = f"Error while. Error: {e}"
        finally:
            con.close()
            return {
                'msg': msg, 
                'request':booking_request}

@app.route('/schedule', methods=['GET'])
def schedule():
    con = sqlite3.connect("database.db")
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM booking_request")
        booking_list = cur.fetchall()
        msg = 'Schedule list.'
    except Exception as e:
        msg = f"Error while. Error: {e}"
    finally:
        con.close()
        return {
            'msg': msg, 
            'request':booking_list}


@app.route('/status/<num_request>', methods=['GET'])
def method_name(num_request):
    status = 'PENDENTE'
    con = sqlite3.connect("database.db")
    try:
        cur = con.cursor()
        cur.execute("SELECT accepted FROM booking_request WHERE num_request=?",(num_request,))
        statusFound = cur.fetchone()
        msg = 'Status found.'
        if statusFound[0] == 1:
            status = 'ACEITO'
        else:
            status = 'REJEITADO'
    except Exception as e:
        msg = f"Error while. Error: {e}"
    finally:
        con.close()
        return {
            'msg': msg, 
            'status':status}

if __name__ == '__main__':
    app.run(debug=True)