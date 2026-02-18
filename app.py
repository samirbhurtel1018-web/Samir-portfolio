from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/contact', methods=['GET','POST'])
def contact():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        conn = sqlite3.connect('messages.db')
        c = conn.cursor()

        c.execute("INSERT INTO messages (name,email,message) VALUES (?,?,?)",
                  (name,email,message))

        conn.commit()
        conn.close()

        return "Message sent successfully"

    return render_template('contact.html')


def create_table():

    conn = sqlite3.connect('messages.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    message TEXT)
    ''')

    conn.commit()
    conn.close()

create_table()

if __name__ == '__main__':
    app.run(debug=True)
