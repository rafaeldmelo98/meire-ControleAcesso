import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

conn = sqlite3.connect('database.db')
conn.execute('''CREATE TABLE IF NOT EXISTS users (user TEXT, password TEXT)''')


# Rotas
@app.route('/')
def home():
    return render_template('index.html')


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


if __name__ == '__main__':
    app.run(debug=True)
