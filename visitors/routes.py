from flask import Blueprint, render_template, request, redirect, url_for, session
from app import mysql

visitors_bp = Blueprint('visitors', __name__)

@visitors_bp.route('/visitors', methods=['GET', 'POST'])
def visitors():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM visitors")
    visitors = cur.fetchall()
    cur.close()

    return render_template('visitors.html', visitors=visitors)


@visitors_bp.route('/addvisitor')
def addVisitor():
    return render_template('addvisitor.html')


@visitors_bp.route('/addnewvisitor', methods=['GET', 'POST'])
def addnewvisitor():

    vname = request.form['name']
    vemail = request.form['email']
    vage = request.form['age']

    cur =mysql.connection.cursor()
    cur.execute("INSERT INTO visitors(name, email, age) VALUES (%s, %s, %s)", (vname, vemail, vage))
    mysql.connect.commit()
    cur.close

    return redirect(url_for('visitors.visitors'))


@visitors_bp.route('/vedit/<int:id>', methods=['POST', 'GET'])
def vedit(id):

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM visitors WHERE id = %s", (id,))
    visitor = cur.fetchone()
    cur.close()

    return render_template('vupdate.html', visitor = visitor)

@visitors_bp.route('/vupdate', methods=['GET', 'POST'])
def vupdate():

    vname = request.form['vname']
    vemail = request.form['vemail']
    vage = request.form['vage']
    vid = request.form['vid']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE visitors SET name = %s, email = %s, age = %s WHERE id = %s", (vname, vemail, vage, vid))
    mysql.connect.commit()

    return redirect(url_for('visitors.vedit', id=vid))


@visitors_bp.route('/vdelete/<int:id>', methods=['GET', 'POST'])
def vdelete(id):

    cur = mysql.connect.cursor()
    cur.execute("DELETE FROM visitors WHERE id =%s", (id,))
    mysql.connect.commit()
    cur.close()

    return redirect(url_for('visitors.visitors'))
