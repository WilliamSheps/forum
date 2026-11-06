from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash
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
    return 'Startsidan kommer<a href="/register">Skapa konto</a>'


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    success = False

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        name = request.form.get('display_name', '').strip()
        password = request.form.get('password', '')

        if username == '' or name == '' or len(password) < 4:
            error = 'Fyll i alla fält. Lösenordet måste vara minst 4 tecken.'
        else:
            db = get_db()
            with db.cursor() as cur:
                cur.execute('SELECT id FROM users WHERE username = %s', (username,))
                if cur.fetchone():
                    error = 'Användarnamnet är upptaget.'
                else:
                    hashed = generate_password_hash(password)
                    cur.execute(
                        'INSERT INTO users (username, password, name) VALUES (%s, %s, %s)',
                        (username, hashed, name),
                    )
                    db.commit()
                    success = True
            db.close()

    return render_template('register.html', error=error, success=success)


if __name__ == '__main__':
    app.run(debug=True)