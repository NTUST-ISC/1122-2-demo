from flask import Flask, request, jsonify, make_response, render_template, redirect
import sqlite3
import execDB
import jwt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.after_request
def apply_caching(response):
    # 移除 Permissions-Policy 头
    response.headers.remove('Permissions-Policy')
    return response

@app.route("/")
def home():
    conn = sqlite3.connect("attackMe.db")
    conn.row_factory = execDB.dict_factory
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM post")
    return render_template("home.html",postList = cursor.fetchall())

@app.route("/newPost")
def postPage():
    return render_template("newPost.html")

@app.route("/post")
def post():
    content = request.args.get("content")
    user_id = request.args.get("user_id")
    post_id = request.args.get("id")
    return render_template("post.html",content = content,user_id = user_id,post_id = post_id)

@app.route("/login")
def loginPage():
    return render_template("login.html")

@app.route("/signup")
def signupPage():
    return render_template("signup.html")

@app.route("/api/posts")
def getPosts():
    conn = sqlite3.connect("attackMe.db")
    conn.row_factory = execDB.dict_factory
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM post")
    return jsonify(cursor.fetchall())

@app.route("/api/login" ,methods = ["POST"]) 
def login():
    data = request.form
    try:
        account = data["account"]
        password = data["password"]
    except TypeError:
        data = jwt.decode(request.cookies.get('token'),"secret",algorithms=["HS256"])
        account = data["account"]
        password = data["password"]
    except:
        return {"message" : "missing argument"} , 401

    conn = sqlite3.connect("attackMe.db")
    conn.row_factory = execDB.dict_factory
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM user WHERE account = '{account}' AND password = '{password}'")
    
    if len(users:=cursor.fetchall()) == 0:
        return {"message" : "login failed"}, 400
    
    token = jwt.encode({"account" : account,"password" : password},"secret",algorithm="HS256")
    response = make_response(redirect("/"))
    response.set_cookie('token',token)
    return response

@app.route("/api/signup",methods = ["POST"])
def signup():
    data = request.form
    try:
        account = data["account"]
        password = data["password"]
    except:
        return {"message" : "missing argument"} , 401

    conn = sqlite3.connect("attackMe.db")
    conn.row_factory = execDB.dict_factory
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM user WHERE account = '{account}'")
    if len(cursor.fetchall()) != 0:
        return {"message" : "account already exists"}, 400

    conn.execute(f"INSERT INTO user(account,password) VALUES('{account}','{password}')")
    conn.commit()
    cursor.execute(f"SELECT * FROM user WHERE account = '{account}'")
    return redirect("/login")

@app.route("/api/newPost",methods = ["POST"])
def newPost():
    try:
        data = jwt.decode(request.cookies.get('token'),"secret",algorithms=["HS256"])
        account = data["account"]
        password = data["password"]
        content = request.form["content"]
    except:
        return {"message" : "Please login"} , 401

    conn = sqlite3.connect("attackMe.db")
    conn.row_factory = execDB.dict_factory
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM user WHERE account = '{account}' AND password = '{password}'")

    if len(users:=cursor.fetchall()) == 0:
        return {"message" : "account or password error"}, 400

    conn.execute(f"INSERT INTO post(user_id,content) VALUES('{users[0]['id']}','{content}')")
    conn.commit()
    cursor.execute(f"SELECT * FROM post WHERE id = (SELECT max(id) from post)")
    return redirect("/")

@app.route("/api/delete")
def delete():
    id = request.args.get("id")

    conn = sqlite3.connect("attackMe.db")
    conn.execute(f"DELETE FROM post where id = {id}")
    conn.commit()

    return {"message" : "success"}

if __name__ == "__main__":
    execDB.main()
    app.run(host="0.0.0.0",port = 8080)
