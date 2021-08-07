from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.secret_key = "emeka"
app.permanent_session_lifetime = timedelta(days=5)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("index.html", list_=todo_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    new_task = Todo(title=title, complete=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/complete/<int:todo_id>")
def finish_task(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)