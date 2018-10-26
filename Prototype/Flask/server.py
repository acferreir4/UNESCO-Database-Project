import os
import time
import sqlite3
from flask import Flask, render_template, request, current_app, redirect

app = Flask(__name__)

DB = "flask.db"

@app.route('/')
def main():
    return render_template('pass.html')

@app.route('/submitinput', methods=['GET', 'POST'])
def form():
    if request.method == "POST":
        load = (request.form.get('textinput'), str(time.time()))
        conn = sqlite3.connect(DB)
        conn.cursor().execute('INSERT INTO Messages VALUES (?,?)', load)
        conn.commit()
        return render_template('pass.html', status="Submitted!")

@app.route('/showmsgs', methods=['GET', 'POST'])
def show():
    if request.method == "POST":
        conn = sqlite3.connect(DB)
        msgs = conn.cursor().execute('SELECT * FROM Messages ORDER BY ts').fetchall()
        #msg_dict = {}
        #for msg in msgs:
        #    msg_dict[msg[0]] = msg[1]
        #print(msg_dict)
        return render_template('pass.html', messages=msgs)

if __name__ == "__main__":
    conn = sqlite3.connect(DB)
    conn.cursor().execute('''CREATE TABLE IF NOT EXISTS Messages (msg text, ts text)''')
    msgs = conn.cursor().execute('SELECT * FROM Messages ORDER BY ts').fetchall()
    print(msgs)
    conn.commit()
    app.run()
