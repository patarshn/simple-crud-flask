from flask import Flask,render_template,request,redirect,url_for,flash,session
import sqlite3 as sql
import json
import AuthMiddleware
import Model
app=Flask(__name__)
app.secret_key='secret'




@app.route("/index")
@app.route("/", methods=['GET'])
@AuthMiddleware.login_required
def index():
    data = {
        'page_title' : 'Dashboard',
    }
    print(session)
    return render_template('index.html',data=data)

@app.route("/login", methods=['GET','POST'])
def login():
    # print(request.method)
    # username = request.form['username']
    # password = request.form['password']
    # sql = f"SELECT * FROM users WHERE username ='{username}' and password = '{password}'"
    # Model.cur.execute(sql)
    # res = Model.cur.fetchone()
    
    # return "post";
    if request.method=='GET':
        return render_template('login.html')
    
    if request.method=='POST':
        try:
            username = request.form['username']
            password = request.form['password']
            sql = f"SELECT * FROM users where username = '{username}' and password = '{password}'"
            Model.cur.execute(sql)
            resRow = Model.cur.fetchone()
            if(resRow is None):
                flash('Wrong Password or Username','danger')
                return redirect(url_for('login'))
            resColumn = Model.cur.column_names
            resData  = dict(zip(resColumn,resRow))
            print(resData)
            session['is_login'] = True
            session['users_id'] = resData['users_id']
            session['username'] = resData['username']
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            flash('Server Error','danger')
            return redirect(url_for('login'))
        return "x"
    return render_template('login.html')
        
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))




if __name__=='__main__':
    sess.init_app(app)
    app.debug = True
    app.run()



