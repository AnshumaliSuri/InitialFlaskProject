from flask import Flask,render_template,request,redirect,session
import psycopg2
import os

app = Flask(__name__)
app.secret_key=os.urandom(24)

conn = psycopg2.connect(database = "MyDatabase",
                        user = "postgres",
                        host= 'localhost',
                        password = "Ganesha@12",
                        port = 6996)
cursor = conn.cursor()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def about():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/login')

@app.route('/login_validation',methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    cursor.execute("""SELECT * FROM users WHERE email LIKE '{}' AND password LIKE '{}'"""
                   .format(email,password))

    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return redirect('/home')
    else :
        return redirect('/')

@app.route('/add_user' ,methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')

    # print("Received Name:", name)
    # print("Received Email:", email)
    # print("Received Password:", password)

    # query = """INSERT INTO users (user_id, name, email, password) VALUES (DEFAULT, %s, %s, %s)"""
    # print("SQL Query:", query)
    # cursor.execute(query, (name, email, password))

    cursor.execute("""INSERT INTO users (user_id, name, email, password) VALUES (DEFAULT, %s, %s, %s)""", (name, email,password))
    conn.commit()
    return "User registered successfully"


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)