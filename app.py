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
        cur.execute("SELECT * FROM users")
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
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (name, password))
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
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cur.fetchone()
    cur.close()
    return render_template('edit.html', user=user)


@app.route('/update', methods=['GET','POST'])
def updateUser():
    if request.method == 'POST':
        id          = request.form['id']
        name        = request.form['name']
        username    = request.form['username']
        email       = request.form['email']
        password    = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET name = %s, username = %s, email = %s, password = %s WHERE id = %s", (name, username, email, password, id))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('editUser', id=id))


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def deleteUser(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/adduser')
def addUser():
    return render_template('adduser.html')

@app.route('/insertnewuser', methods=['POST'])
def addnewuser():
    name        = request.form['name']
    username    = request.form['username']
    email       = request.form['email']
    password    = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(name, username, email, password) VALUES(%s, %s, %s, %s)", (name, username, email, password))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))


@app.route('/visitors', methods=['GET', 'POST'])
def visitors():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM visitors")
    visitors = cur.fetchall()
    cur.close()


    return render_template('visitors.html', visitors=visitors)


@app.route('/addvisitor')
def addVisitor():
    return render_template('addvisitor.html')



if __name__ == '__main__':
    app.run(debug=True)
