from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from flask import abort
from flask import url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'UserDatabase.db'

def get_data():
        db = getattr(g, '_database,', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
            cursor = db.cursor()
            cursor.execute("select * from Users")
        return cursor.fetchall()
def get_db():
    db = getattr(g, '_database,', None)
    db = g._database = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    return cursor

def get_post(post_id):
    conn = get_db()
    post = conn.execute('SELECT * FROM Users WHERE Id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route("/", methods=["GET"])
def index(name=None):
        data = get_data()
        return render_template("index.html", all_data=data, selected_user=("", "", ""))
@app.route("/<user>", methods=["GET"])
def userSearch(user):
        the_user = get_post(user)
        data = get_data()
        return render_template("index.html", all_data=data, selected_user=the_user)
@app.route("/submituser", methods=["POST"])
def add(name=None):
        app.logger.info('testing info log')
        if request.method == "POST":
            db = getattr(g, '_database,', None)
            db = g._database = sqlite3.connect(DATABASE)
            cursor = db.cursor()
            newUser = (int(request.form['id']), request.form['name'], int(request.form['points']))
            try:
                cursor.execute("INSERT INTO Users VALUES (?, ?, ?)", newUser)
                db.commit()
                db.close()
                return redirect("/")
            except:
                return redirect("/")
            
@app.route("/edituser", methods=["POST"])
def edit():
     if request.method == "POST":
            db = getattr(g, '_database,', None)
            db = g._database = sqlite3.connect(DATABASE)
            cursor = db.cursor()
            newUser = (request.form['name'], int(request.form['id']), int(request.form['points']), int(request.form['edit_user']))
            try:
                cursor.execute("UPDATE Users SET Name = ?, Id = ?, Points = ?" "WHERE Id = ?", newUser)
                db.commit()
                db.close()
                return redirect("/")
            except:
                return redirect("/")
@app.route("/deleteuser", methods=["POST"])
def delete():
     if request.method == "POST":
            db = getattr(g, '_database,', None)
            db = g._database = sqlite3.connect(DATABASE)
            cursor = db.cursor()
            newUser = (request.form['deleted_user'])
            try:
                cursor.execute("DELETE FROM Users WHERE Id = ?", newUser)
                db.commit()
                db.close()
                return redirect("/")
            except:
                return redirect("/")
@app.route("/searchuser", methods=["POST"])
def search():
     if request.method == "POST":
            searched_user = request.form['searched_user']
            app.logger.info('testing info log ' + searched_user)
            return redirect("/"+searched_user)
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()