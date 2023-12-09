from flask import *
import pymysql

app=Flask(__name__)
app.secret_key='mySecretKey'
connection=pymysql.connect(host="localhost",user="root",database="bookings_db",password="")
@app.route("/")
def Main():
    return "welcome to our application. type the route name in the address bar"
# home code
@app.route("/home",methods=['GET','POST'])
def home():
 return render_template ("index.html")

@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method =='POST':
        # TODO
        # get data from the form
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        confirm_password=request.form['confirm_password']
        # connection already defined
        # input validation

        if not username or not email  or not password or not confirm_password:
            return render_template("account.html",error="please fill all the records") 
        if password !=confirm_password:
            return render_template("account.html",error="password dont match confirm passsword")
        elif " "in username:
            return render_template("account.html",error="username must be one word")

  
        elif '@' not in email:
            return render_template ("account.html",error="email must have @")

        elif len(password) <4:
            return render_template("account.html",error="password must have 4 digits") 
        else:
            # check if the user exists
            sql_check_user='select * from users where username=%s'
            cursor_check_user=connection.cursor()
            cursor_check_user.execute(sql_check_user, username)
            if cursor_check_user.rowcount==1:
              return render_template("account.html",error="Username already exists")

            sql_save='insert into users (username,email,password) values(%s,%s,%s)'
            values=(username,email,password) 
            # cursor function
            cursor_save=connection.cursor()
            # execute the sql query  
            cursor_save.execute(sql_save,values)
            # commit
            connection.commit()
            return render_template("account.html",message="signup successful", active_page="signup", form_type="signup") 
    else:
        return render_template("account.html",  active_page="signup", form_type="signup") 
    
@app.route("/login",methods=['GET','POST'])
def signin():
    #check the method
    if request.method=='POST':
        # TODO
        username=request.form['username']
        password=request.form['password']
        # define the sql query
        sql='select * from users where username=%s and password=%s'
        # create cursor function 
        cursor=connection.cursor()
        # exeucte the qury
        cursor.execute(sql,(username,password))
        # check if user esxits
        if cursor.rowcount==0:
            return render_template("account.html",error="Incorrect login credentials.Try again")
        # create user sessions
        session['key']=username
        # fetch the other columns
        user=cursor.fetchone()
        session['email']=user[1]
        session['phone']=user[2]
        return redirect("/profile")
    # If the request method is GET, render the login page
    else:
     return render_template("account.html",  active_page="login", form_type="login")
# clear the session
@app.route("/profile")
def profile():
    if is_logged_in():
        # Access the user data from the session
        username = session['key']
        email = session['email']
        phone = session['phone']
        
        return render_template("profile.html", username=username, email=email, phone=phone)
    else:
        # Redirect to login if not logged in
        return redirect("/login")

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")

app.run(debug=True,port=80000)