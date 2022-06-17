from flask import Flask,render_template,request,redirect,url_for,flash,session
import sqlite3 as sql
import json

app=Flask(__name__)
app.secret_key='secret'

@app.route("/")
@app.route("/index")
def index():
    data = {
        'page_title' : 'Dashboard',
    }
    print(session)
    return render_template('index.html',data=data);

@app.route("/logout")
def logout():
    return 'logout'

if __name__=='__main__':
    sess.init_app(app)
    app.debug = True
    app.run()



