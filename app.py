from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'secretkey'

app.config['MYSQL_HOST']        = 'localhost'
app.config['MYSQL_USER']        = 'root'
app.config['MYSQL_PASSWORD']    = ''
app.config['MYSQL_DB']          = 'flask_crud'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Check if user is logged in (avoid KeyError)
    if session.get('login') == True:

        # Fetch all users for the table
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, email FROM users")
        users = cur.fetchall()
        cur.close()

        # Always render with users (even if empty)
        return render_template('index.html', users=users)

    # Not logged in, redirect to login page
    return render_template('index.html')




@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        # print(request.form)
        # exit()

        name        = request.form['username']
        email       = request.form['email']
        password    = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, password) VALUES(%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        cur.close()

        if cur.rowcount == 1:
            message = 'You have successfully registered'
            return render_template('login.html', message=message)
        else:
            message = 'Error in registering'

    return render_template('register.html', message=message)



@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        name     = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE name = %s AND password = %s", (name, password))
        user = cur.fetchone()
        cur.close()

        if user:
            session['name']  = user[1].upper()
            session['id']    = user[0]
            session['login'] = True

            return redirect(url_for('index'))

        else:
            message = 'Bad username or password'
            return render_template('login.html', message=message)

    return render_template('login.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def editUser(id):
    return render_template('edit.html')


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def deleteUser(id):
    return render_template('delete.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
