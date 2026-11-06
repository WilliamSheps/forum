from flask import Flask
import pymysql

app = Flask(__name__)
app.secret_key = 'hemligt'

def get_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='forum',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )


@app.route('/')
def index():
    db = get_db()
    with db.cursor() as cur:
        cur.execute('SELECT COUNT(*) AS antal FROM users')
        antal = cur.fetchone()['antal']
    db.close()
    return f'Anslutningen funkar Antal användare: {antal}'


if __name__ == '__main__':
    app.run(debug=True)