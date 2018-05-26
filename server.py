import sqlite3
import requests
from flask import Flask
from flask import jsonify
app = Flask(__name__)

@app.route('/attendance/<code>', methods=['GET'])
def attendance(code):
    return check(code, 2, "attendance")

@app.route('/food1/<code>', methods=['GET'])
def food1(code):
    return check(code, 3, "food1")

@app.route('/food2/<code>', methods=['GET'])
def food2(code):
    return check(code, 4, "food2")

@app.route('/food3/<code>', methods=['GET'])
def food3(code):
    return check(code, 5, "food3")

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(result=get_table_values())

@app.route('/update', methods=['POST'])
def update():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    rows = get_sheets()
    for row in rows:
        c.execute('''INSERT OR REPLACE INTO users VALUES (''' +
            '\'' + row[0] + '\',' +
            '\'' + row[1] + '\',' +
            '\'' + row[2] + '\',' +
            '\'' + row[3] + '\',' +
            '\'' + row[4] + '\',' +
            '\'' + row[5] + '\');')
    conn.commit()
    conn.close()
    return "ok"

def check(code, pos, col_name):
    users = get_table_values()
    for user in users:
        if user[1] == code:
            if user[pos] == 0:
                accept(code, col_name)
                return jsonify(result=1,name=user[0])
            else:
                return jsonify(result=2,name=user[0])
    return jsonify(result=-1,name=user[0])

def start_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        name text NOT NULL, 
        code text NOT NULL PRIMARY KEY, 
        attendance integer,
        food1 integer,
        food2 integer,
        food3 integer
        ); ''')
    update()
    conn.close()

def get_sheets():
    r = requests.get('https://sheets.googleapis.com/v4/spreadsheets/1xFohoN8VWofuKfI-qqsAn8nQSzpllbUhFJlQTblhV7c/values/A1:F100?key=AIzaSyDCoN8AQGQM5FYZZ2mC5QhnqT4Ldbho8hg')
    return r.json()['values']

def get_table_values():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    result = [row for row in c.execute("SELECT * FROM USERS")]
    conn.close()
    return result

def accept(code, pos):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("UPDATE users SET " + pos + " = 1 WHERE code = '" + code + "'")
    conn.commit()
    conn.close()

start_db()
