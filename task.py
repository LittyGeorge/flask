from flask import *
import sqlite3
app=Flask(__name__)
app.secret_key="abcde"

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/reg")
def reg():
    return render_template("reg.html")




@app.route('/registfunc',methods=['POST'])
def registfunc():
    firstname=request.form['firstname']
    lastname=request.form['lastname']
    phno=request.form['phone']
    age=request.form['age']
    usertype=request.form['usertype']
    username=request.form['username']
    password=request.form['password']
    con=sqlite3.connect('task.db')
    cursor1=con.cursor()
    cursor1.execute("insert into users(username,password,usertype)values(?,?,?)",(username,password,usertype))
    uid=cursor1.lastrowid
    if usertype=="student":
        cursor1.execute("insert into stud(firstname,lastname,phno,age,userid)values(?,?,?,?,?)",(firstname,lastname,phno,age,uid))
    else:
        cursor1.execute("insert into teacher(firstname,lastname,phno,age,userid)values(?,?,?,?,?)",(firstname,lastname,phno,age,uid))
    con.commit()
    return redirect("loginpage")

@app.route('/loginpage')
def loginpage():
    return render_template("login.html")

@app.route("/login",methods=['POST'])
def login():
    username = request.form["username"]
    password = request.form["password"]
    session["username"] = username
    session["password"] = password
    con=sqlite3.connect('task.db')
    con.row_factory=sqlite3.Row
    cursor3=con.cursor()
    cursor3.execute("select * from users where username=? and password=?",(username,password))
    us=cursor3.fetchone()
    if us["username"]==username and us["password"]==password and us["is_approve"]==1:
        if us["usertype"]=="student":
            print(us["usertype"])
            return render_template("stud_home.html")
        elif us["usertype"]=="teacher":
            print(us["usertype"])
            return render_template("teach_home.html")
            
        else:
            # print(us["usertype"])
            return render_template("admin.html")
    else:
        return "Invaid credentials"
    
@app.route("/logout")
def logout():
    session.pop("username")
    session.pop("password")
    session.clear()
    return redirect("loginpage")

@app.route("/studapprove")
def studapprove():
    if 'username' not in session and session['username'] != 'admin':
        return redirect(url_for('login'))
    con=sqlite3.connect('task.db')
    con.row_factory=sqlite3.Row
    cursor2=con.cursor()
    cursor2.execute("select users.userid,users.username,stud.* from users join stud where users.userid=stud.userid and users.is_approve=0")
    st=cursor2.fetchall()
    return render_template("admin_stud_approve.html",students=st)

@app.route('/get_approval_stud/<int:id>',methods=['POST'])
def get_approval(id):
    if 'username' not in session and session['username'] != 'admin':
        return redirect(url_for('login'))
    con=sqlite3.connect('task.db')
    con.row_factory=sqlite3.Row
    cursor3=con.cursor()
    isApprove=request.form["approved"]
    cursor3.execute("update users set is_approve=? where userid=?",(isApprove,id))
    con.commit()
    return redirect('/studapprove')

@app.route("/teachapprove")
def teachapprove():
    if 'username' not in session and session['username'] != 'admin':
        return redirect(url_for('login'))
    con=sqlite3.connect('task.db')
    con.row_factory=sqlite3.Row
    cursor4=con.cursor()
    cursor4.execute("select users.userid,users.username,teacher.* from users join teacher where users.userid=teacher.userid and users.is_approve=0")
    t=cursor4.fetchall()
    return render_template("admin_teach_approve.html",teachers=t)

@app.route('/get_approval_teach/<int:id>',methods=['POST'])
def get_approval_teach(id):
    if 'username' not in session and session['username'] != 'admin':
        return redirect(url_for('login'))
    con=sqlite3.connect('task.db')
    con.row_factory=sqlite3.Row
    cursor5=con.cursor()
    isApprove=request.form["approved"]
    cursor5.execute("update users set is_approve=? where userid=?",(isApprove,id))
    con.commit()
    return redirect('/teachapprove')


@app.route('/admin_view_students')
def admin_view_students():
    if 'username' not in session and session['username'] != 'admin':
        return redirect(url_for('login'))
    con=sqlite3.connect('task.db')
    con.row_factory=sqlite3.Row
    cursor6=con.cursor()
    cursor6.execute("Select * from stud")
    stud=cursor6.fetchall()
    return render_template("admin_viewstud.html",stud=stud)

@app.route("/delete_stud/<int:id>",methods=['POST'])
def delete_stud(id):
    if 'username' not in session and session['username'] != 'admin':
        return redirect(url_for('login'))
    con=sqlite3.connect('task.db')
    con.row_factory=sqlite3.Row
    cursor7=con.cursor()
    cursor7.execute("select * from stud where studid=?",(id,))
    st=cursor7.fetchone()
    userid=st["userid"]
    cursor7.execute("delete from stud where studid=?",(id,))
    cursor7.execute("delete from users where userid=?",(userid,))
    con.commit()
    return redirect('/admin_view_students')


@app.route('/admin_view_teachers')
def admin_view_teachers():
    if 'username' not in session and session['username'] != 'admin':
        return redirect(url_for('login'))
    con=sqlite3.connect('task.db')
    con.row_factory=sqlite3.Row
    cursor8=con.cursor()
    cursor8.execute("Select * from teacher")
    teach=cursor8.fetchall()
    return render_template("admin_viewteacher.html",teach=teach)

@app.route("/delete_teach/<int:id>",methods=['POST'])
def delete_teach(id):
    if 'username' not in session and session['username'] != 'admin':
        return redirect(url_for('login'))
    con=sqlite3.connect('task.db')
    con.row_factory=sqlite3.Row
    cursor9=con.cursor()
    cursor9.execute("select * from teacher where teachid=?",(id,))
    t=cursor9.fetchone()
    userid=t["userid"]
    cursor9.execute("delete from teacher where teachid=?",(id,))
    cursor9.execute("delete from users where userid=?",(userid,))
    con.commit()
    return redirect('/admin_view_teachers')


print("hello")
print("hai")
print("flaskkkk")
print('welcome')
if __name__=="__main__":
    app.run(debug=True)