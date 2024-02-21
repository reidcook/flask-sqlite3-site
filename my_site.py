from flask import Flask
from flask import render_template
from flask import g
import sqlite3

app = Flask(__name__)

DATABASE = 'names.db'

def get_db():
        db = getattr(g, '_database,', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
            cursor = db.cursor()
            cursor.execute("select * from tbl1")
        return cursor.fetchall()

@app.route("/")
def index(name=None):
        data = get_db()
        return render_template("index.html", all_data=data)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()