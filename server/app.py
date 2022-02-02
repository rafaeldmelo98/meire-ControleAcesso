import sqlite3
from flask import Flask, request

app = Flask(__name__)

conn = sqlite3.connect('database.db')
conn.execute('''CREATE TABLE IF NOT EXISTS users (user TEXT, password TEXT, key_user TEXT)''')
conn.execute('''CREATE TABLE IF NOT EXISTS booking_request (num_request TEXT, key_user TEXT, 
date_request TEXT, accepted INTEGER)''')
conn.close()


# Rotas
@app.route('/')
def home():
    return {'msg': 'Página inicial'}


@app.route('/login', methods=['GET'])
def login():
    if request.method == 'GET':
        try:
            user = request.args['user']
            password = request.args['password']
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE user=?", (user,))
                user_db = cur.fetchone()
                if user_db[1] == password:
                    msg = 'Usuário logado.'
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
                'login?': login}


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        try:
            user = request.args['user']
            password = request.args['password']

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users(user, password) \
                    VALUES(?, ?)", (user, password))
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
    if request.method == 'POST':
        try:
            key_user = request.args['user']
            data_request = request.args['date_request']

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute('SELECT COUNT(*) FROM booking_request')
                id = cur.fetchone()
                cur.execute('INSERT INTO booking_request(num_request, key_user, date_request, accepted) \
                VALUES (?,?,?,0)', ((id+1),key_user,data_request))
                con.commit()
                msg = 'Date booked!'
        except Exception as e:
            con.rollback()
            msg = f"Error while. Error: {e}"
        finally:
            con.close()
            return {'msg': msg}
    if request.method == 'GET':
        pass


if __name__ == '__main__':
    app.run(debug=True)
