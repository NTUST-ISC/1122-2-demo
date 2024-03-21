from urllib import request
import flask 
import sqlite3
import execDB
from flask_cors import CORS


app = flask.Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "home"

@app.route("/login" ,methods = ["POST"]) 
def login():
    data = flask.request.json
    try:
        account = data["account"]
        password = data["password"]
    except:
        return {"message" : "missing argument"} , 401


    conn = sqlite3.connect("attackMe.db")
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM user WHERE account = '{account}' AND password = '{password}'")
    
    if len(users:=cursor.fetchall()) == 0:
        return {"message" : "login failed"}, 400
    return users[0]

@app.route("/signup",methods = ["POST"])
def signup():
    data = flask.request.json
    try:
        account = data["account"]
        password = data["password"]
    except:
        return {"message" : "missing argument"} , 401


    conn = sqlite3.connect("attackMe.db")
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM user WHERE account = '{account}'")
    if len(cursor.fetchall()) != 0:
        return {"message" : "account already exists"}, 400

    conn.execute(f"INSERT INTO user(account,password) VALUES('{account}','{password}')")
    conn.commit()
    cursor.execute(f"SELECT * FROM user WHERE account = '{account}'")
    return cursor.fetchall()[0]


@app.route("/post",methods = ["POST"])
def post():
    data = flask.request.json
    try:
        account = data["account"]
        password = data["password"]
        content = data["content"]
    except:
        return {"message" : "missing argument"} , 401

    conn = sqlite3.connect("attackMe.db")
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM user WHERE account = '{account}' AND password = '{password}'")

    if len(users:=cursor.fetchall()) == 0:
        return {"message" : "account or password error"}, 400

    conn.execute(f"INSERT INTO post(user_id,content) VALUES('{users[0]['id']}','{content}')")
    conn.commit()
    cursor.execute(f"SELECT * FROM post WHERE id = (SELECT max(id) from post)")
    return cursor.fetchall()[0]

@app.route("/getPost",methods = ["GET"])
def getPost():
    conn = sqlite3.connect("attackMe.db")
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM post")

    return flask.jsonify(cursor.fetchall())

def dict_factory(cursor, row):
    dict = {}
    for idx, col in enumerate(cursor.description):
        dict[col[0]] = row[idx]
    return dict


@app.route("/delete")
def delete():
    id = flask.request.args.get("id")

    conn = sqlite3.connect("attackMe.db")
    conn.execute(f"DELETE FROM post where id = {id}")
    conn.commit()

    return {"message" : "success"}



if __name__ == "__main__":
    execDB.main()
    app.run(host="0.0.0.0",port = 8080)
