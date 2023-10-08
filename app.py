from flask import Flask, render_template, url_for, redirect, request, flash
from flask_mysqldb import MySQL  # mysql import

app = Flask(__name__)  # FLASK OBJECT=CURRENT PY FILE
# MYSQL CONNECTION
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"  # default name
app.config["MYSQL_PASSWORD"] = "charan@0504"
app.config["MYSQL_DB"] = "crud"
# normally array it is difficult to use so this
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


# Loading Home Page
@app.route("/")  # home page
def home():
    con = mysql.connection.cursor()  # connect database
    sql = "SELECT * FROM users"
    con.execute(sql)
    res = con.fetchall()  # all records
    # return html page,res o/p  variable  pass datas
    return render_template("home.html", datas=res)

# New User


@app.route("/addUsers", methods=['GET', 'POST'])  # addusers html page go,
def addUsers():
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        age = request.form['age']
        con = mysql.connection.cursor()
        sql = "insert into users(NAME,CITY,AGE) value (%s,%s,%s)"
        con.execute(sql, [name, city, age])  # upper data sql pass 3val as list
        mysql.connection.commit()  # db store
        con.close()
        flash('User Details Added')  # details updated flash message
        # 1details add redirect to home page,import redirect
        return redirect(url_for("home"))
    return render_template("addUsers.html")

# update User


@app.route("/editUser/<string:id>", methods=['GET', 'POST'])
def editUser(id):  # primary key
    con = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        age = request.form['age']
        sql = "update users set NAME=%s,CITY=%s,AGE=%s where ID=%s"
        con.execute(sql, [name, city, age, id])
        mysql.connection.commit()
        con.close()
        flash('User Detail Updated')
        return redirect(url_for("home"))
        con = mysql.connection.cursor()

    sql = "select * from users where ID=%s"
    con.execute(sql, [id])
    res = con.fetchone()  # single data
    return render_template("editUser.html", datas=res)
# Delete User


@app.route("/deleteUser/<string:id>", methods=['GET', 'POST'])
def deleteUser(id):
    con = mysql.connection.cursor()
    sql = "delete from users where ID=%s"
    con.execute(sql, id)
    mysql.connection.commit()
    con.close()
    flash('User Details Deleted')
    return redirect(url_for("home"))


if (__name__ == '__main__'):
    app.secret_key = "abc123"  # for flash message
    app.run(debug=True)  # run flask objecr,debug T -auto debug
