from flask import Flask,render_template,request,redirect,url_for,flash,session
import sqlite3 as sql
import json
import AuthMiddleware
import Model
import datetime
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
    if request.method=='GET':
        return render_template('login.html')
    
    if request.method=='POST':
        try:
            username = request.form['username']
            password = request.form['password']
            sql = f"SELECT * FROM users where username = '{username}' and password = '{password}' and deleted_at is NULL"
            Model.cur.execute(sql)
            resRow = Model.cur.fetchone()
            if(resRow is None):
                flash('Wrong Password or Username','danger')
                return redirect(url_for('login'))
            # resColumn = Model.cur.column_names
            # resData  = dict(zip(resColumn,resRow))
            # print(resData)
            session['is_login'] = True
            session['users_id'] = resRow['users_id']
            session['username'] = resRow['username']
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            flash('Server Error','danger')
            return redirect(url_for('login'))
    return render_template('login.html')
        
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/karyawan",methods=['GET'])
@AuthMiddleware.login_required
def karyawan():
    if request.method=='GET':
        data = {
            'page_title' : 'Karyawan',
        }
        try:
            users_id = session['users_id']
            sql = f"SELECT * FROM users where users_id = '{users_id}' and deleted_at is NULL"
            Model.cur.execute(sql)
            resRow = Model.cur.fetchone()
            # resColumn = Model.cur.column_names
            # resData  = dict(zip(resColumn,resRow))
            # print(resData)
            print(resRow)
            data['users'] = resRow
        except Exception as e:
            print(e)
        print(data)
        return render_template('karyawan/index.html',data=data)
    return render_template('karyawan/index.html')

@app.route("/absensi",methods=['GET'])
@AuthMiddleware.login_required
def absensi():
    data = {
        'page_title' : 'Absensi',
    }
    if request.method=='GET':
        data = {
            'page_title' : 'Absensi',
        }
        try:
            users_id = session['users_id']
            sql = f"SELECT * FROM absensis where user_id = '{users_id}' and deleted_at is NULL"
            Model.cur.execute(sql)
            resRow = Model.cur.fetchall()
            print(resRow)
            data['absensis'] = resRow
        except Exception as e:
            print(e)
        print(data)
        return render_template('absensi/index.html',data=data)
    return render_template('absensi/index.html',data=data)



@app.route("/absensi/add",methods=['GET','POST'])
@AuthMiddleware.login_required
def absensi_add():
    data = {
        'page_title' : 'Tambah Absensi',
    }
    if request.method=='GET':
        # try:
        #     data = {
        #         'page_title' : 'Tambah Absensi',
        #     }
        # except Exception as e:
        #     print(e)
        #     flash('Error Access Add Absensi')
        #     return redirect(url_for('absensi'))
        # return render_template('absensi/add.html',data=data)
        return redirect(url_for('absensi'))
    if request.method=='POST':
        data = {
            'page_title' : 'Tambah Absensi',
        }
        users_id = session['users_id']
        try:
            if(request.form.get('check') is None):
                pass
            if(request.form['check'] == 'in'):
                today = str(datetime.date.today())
                sql = f"SELECT * FROM absensis where date(check_in) = '{today}' and user_id = '{users_id}' and deleted_at is NULL"
                print(sql)
                Model.cur.execute(sql)
                rowCount = Model.cur.rowcount
                print(rowCount)
                if(rowCount > 0):
                    msg = f"anda sudah check in hari ini";
                    flash(msg,'danger')
                    return redirect(url_for('absensi'))
                check_in = str(datetime.datetime.now())
                created_at = str(datetime.datetime.now())
                sql = f"INSERT INTO absensis VALUES(NULL,'{users_id}','{check_in}',NULL,'{created_at}',NULL)"
                Model.cur.execute(sql)
                if(Model.cur.rowcount):
                    msg = f"{Model.cur.rowcount} row inserted";
                    flash(msg,'success')
                else:
                    msg = f"checkin failed";
                    flash(msg,'danger')
            if(request.form['check'] == 'out'):
                check_out = str(datetime.datetime.now())
                absensi_id = request.form['absensi_id']
                sql = f"UPDATE absensis SET check_out = '{check_out}' where user_id = '{users_id}' and absensis_id = '{absensi_id}'"
                Model.cur.execute(sql)
                if(Model.cur.rowcount):
                    msg = f"{Model.cur.rowcount} row update";
                    flash(msg,'success')
                else:
                    msg = f"checkout failed";
                    flash(msg,'danger')
            return redirect(url_for('absensi'))
        except Exception as e:
            print(e)
            flash('Server Error','danger')
            return redirect(url_for('absensi'))
    return redirect(url_for('absensi'))

@app.route("/absensi/delete",methods=['POST'])
@AuthMiddleware.login_required
def absensi_delete():
    data = {
        'page_title' : 'Delete Absensi',
    }
    if request.method=='POST':
        data = {
            'page_title' : 'Delete Absensi',
        }
        try:
            absensi_id = request.form['absensi_id']
            user_id = session['users_id']
            deleted_at = str(datetime.datetime.now())
            sql = f"UPDATE absensis SET deleted_at = '{deleted_at}' where absensis_id = '{absensi_id}' and user_id = '{user_id}' and deleted_at is NULL"
            Model.cur.execute(sql)
            if(Model.cur.rowcount):
                msg = f"{Model.cur.rowcount} row deleted";
                flash(msg,'success')
            else:
                msg = f"delete failed";
                flash(msg,'danger')
            return redirect(url_for('absensi'))
        except Exception as e:
            print(e)
            flash('Server Error','danger')
            return redirect(url_for('absensi'))

@app.route("/aktivitas",methods=['GET'])
@AuthMiddleware.login_required
def aktivitas():
    if request.method=='GET':
        data = {
            'page_title' : 'Aktivitas',
        }
        try:
            users_id = session['users_id']
            sql = f"SELECT * FROM aktivitass where user_id = '{users_id}' and deleted_at is NULL"
            Model.cur.execute(sql)
            resRow = Model.cur.fetchall()
            # resColumn = Model.cur.column_names
            # resRowLen = len(resRow)
            # resData = [ dict(zip(resColumn,resRow[i])) for i in range(resRowLen) ]
            # print(resData)
            print(resRow)
            data['aktivitass'] = resRow
        except Exception as e:
            print(e)
        print(data)
        return render_template('aktivitas/index.html',data=data)
    return render_template('aktivitas/index.html')

@app.route("/aktivitas/add",methods=['GET','POST'])
@AuthMiddleware.login_required
def aktivitas_add():
    data = {
        'page_title' : 'Tambah Aktivitas',
    }
    if request.method=='GET':
        return redirect(url_for('aktivitas'))
    if request.method=='POST':
        data = {
            'page_title' : 'Tambah Aktivitas',
        }
        users_id = session['users_id']
        nama_aktivitas = request.form['nama_aktivitas']
        tanggal_aktivitas = request.form['tanggal_aktivitas']
        waktu_aktivitas = request.form['waktu_aktivitas']
        status_aktivitas = 'on-going'
        created_at = str(datetime.datetime.now())
        sql = f"INSERT INTO aktivitass VALUES(NULL,'{users_id}','{nama_aktivitas}','{tanggal_aktivitas}','{waktu_aktivitas}','{status_aktivitas}','{created_at}',NULL)"
        Model.cur.execute(sql)
        if(Model.cur.rowcount):
            msg = f"{Model.cur.rowcount} row inserted";
            flash(msg,'success')
        else:
            msg = f"tambah aktivitas failed";
            flash(msg,'danger')
        return redirect(url_for('aktivitas'))
        try:
            nama_aktivitas = request.name['nama_aktivitas']
            tanggal_aktivitas = request.name['tanggal_aktivitas']
            waktu_aktivitas = request.name['waktu_aktivitas']
            status_aktivitas = 'on-going'
            created_at = str(datetime.datetime.now())
            sql = f"INSERT INTO aktivitass VALUES(NULL,'{users_id}','{nama_aktivitas}','{tanggal_aktivitas}','{waktu_aktivitas}','{status_aktivitas}','{created_at}',NULL)"
            Model.cur.execute(sql)
            if(Model.cur.rowcount):
                msg = f"{Model.cur.rowcount} row inserted";
                flash(msg,'success')
            else:
                msg = f"tambah aktivitas failed";
                flash(msg,'danger')
            return redirect(url_for('aktivitas'))
        except Exception as e:
            print(e)
            flash('Server Error','danger')
            return redirect(url_for('aktivitas'))
    return redirect(url_for('aktivitas'))

@app.route("/aktivitas/edit",methods=['POST'])
@AuthMiddleware.login_required
def aktivitas_edit():
    data = {
        'page_title' : 'Edit Aktivitas',
    }
    user_id = session['users_id']
    if request.method=='POST':
        try:
            aktivitass_id = request.form['aktivitass_id']
            nama_aktivitas = request.form['nama_aktivitas']
            tanggal_aktivitas = request.form['tanggal_aktivitas']
            waktu_aktivitas = request.form['waktu_aktivitas']
            status_aktivitas  = request.form['status_aktivitas']
            deleted_at = str(datetime.datetime.now())
            sql = f'''UPDATE aktivitass SET 
                nama_aktivitas = '{nama_aktivitas}' , 
                tanggal_aktivitas = '{tanggal_aktivitas}' , 
                waktu_aktivitas = '{waktu_aktivitas}' ,
                status_aktivitas = '{status_aktivitas}'
                where aktivitass_id = '{aktivitass_id}' and user_id = '{user_id}' and deleted_at is NULL'''
            print(sql)
            Model.cur.execute(sql)
            if(Model.cur.rowcount):
                msg = f"{Model.cur.rowcount} row updated";
                flash(msg,'success')
            else:
                msg = f"delete failed";
                flash(msg,'danger')
            return redirect(url_for('aktivitas'))
        except Exception as e:
            print(e)
            flash('Server Error','danger')
            return redirect(url_for('aktivitas'))

@app.route("/aktivitas/delete",methods=['POST'])
@AuthMiddleware.login_required
def aktivitas_delete():
    data = {
        'page_title' : 'Delete Absensi',
    }
    if request.method=='POST':
        data = {
            'page_title' : 'Delete Absensi',
        }
        try:
            aktivitas_id = request.form['aktivitas_id']
            user_id = session['users_id']
            deleted_at = str(datetime.datetime.now())
            sql = f"UPDATE aktivitass SET deleted_at = '{deleted_at}' where aktivitass_id = '{aktivitas_id}' and user_id = '{user_id}' and deleted_at is NULL"
            Model.cur.execute(sql)
            if(Model.cur.rowcount):
                msg = f"{Model.cur.rowcount} row deleted";
                flash(msg,'success')
            else:
                msg = f"delete failed";
                flash(msg,'danger')
            return redirect(url_for('aktivitas'))
        except Exception as e:
            print(e)
            flash('Server Error','danger')
            return redirect(url_for('aktivitas'))

if __name__=='__main__':
    # sess.init_app(app)
    app.debug = True
    app.run()



