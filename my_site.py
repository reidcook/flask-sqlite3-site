from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from flask import abort
import sqlite3

app = Flask(__name__)

DATABASE = 'names.db'

def get_data():
        db = getattr(g, '_database,', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
            cursor = db.cursor()
            cursor.execute("select * from tbl1")
        return cursor.fetchall()
def get_db():
    db = getattr(g, '_database,', None)
    db = g._database = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    return cursor

def get_post(post_id):
    conn = get_db()
    post = conn.execute('SELECT * FROM tbl1 WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route("/", methods=["GET"])
def index(name=None):
        data = get_data()
        return render_template("index.html", all_data=data)
@app.route("/submituser", methods=["POST"])
def add(name=None):
        app.logger.info('testing info log')
        if request.method == "POST":
            db = getattr(g, '_database,', None)
            db = g._database = sqlite3.connect(DATABASE)
            cursor = db.cursor()
            newUser = (request.form['name'], int(request.form['id']), int(request.form['points']))
            try:
                cursor.execute("INSERT INTO tbl1 VALUES (?, ?, ?)", newUser)
                db.commit()
                db.close()
                app.logger.info("hello")
                return redirect("/")
            except:
                return "There was an error that occured"
            
@app.route("/edituser", methods=["POST"])
def edit():
     if request.method == "POST":
            db = getattr(g, '_database,', None)
            db = g._database = sqlite3.connect(DATABASE)
            cursor = db.cursor()
            newUser = (request.form['name'], int(request.form['id']), int(request.form['points']), int(request.form['edit_user']))
            try:
                cursor.execute("UPDATE tbl1 SET Name = ?, Id = ?, Points = ?" "WHERE Id = ?", newUser)
                db.commit()
                db.close()
                app.logger.info("hello")
                return redirect("/")
            except:
                return "There was an error that occured"
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()