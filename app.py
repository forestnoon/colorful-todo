from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://drzhpnvaysjdcq:2c31e06af27a1ba954c00c1e0dc9441be0d3018fe2d404421b917c8ec55e5da6@ec2-34-192-122-0.compute-1.amazonaws.com:5432/d8jgvj9lv98s4j"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# モデル
class Task(db.Model):

  __tablename__ = "tasks"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  date = db.Column(db.Integer)
  task_type = db.Column(db.String(200))
  priority = db.Column(db.Integer)
  title = db.Column(db.String(200))
  text = db.Column(db.String(200))


# index.html
@app.route('/', methods=['GET'])
def index():
  tasks = Task.query.all()
  return render_template("index.html", tasks=tasks)

# /create
@app.route('/create', methods=['POST'])
def create():
  task = Task()
  task.date = str(datetime.today().year) + "/" + str(datetime.today().month) + "/" + str(datetime.today().day) + " " + str(datetime.today().hour) + "時" + str(datetime.today().minute) + "分"
  task.task_type = request.form.get('task_type')
  task.priority = request.form.get('priority')
  task.title = request.form.get('title')
  task.text = request.form.get('text')
  
  db.session.add(task)
  db.session.commit()

  return redirect(url_for('.index'))


# /delete
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
  task = Task.query.get(id)
  
  db.session.delete(task) 
  db.session.commit()
  db.session.close()
  # tasks = Task.query.all()
  return redirect(url_for('.index'))


# /edit
@app.route('/edit/<int:id>', methods=['GET'])
def edit(id):
  task = Task.query.get(id)

  return render_template('edit.html', task=task)


# /update
@app.route('/update/<int:id>', methods=["POST"])
def update(id):
   
    task = Task.query.get(id)
    
    task.date = str(datetime.today().year) + "/" + str(datetime.today().month) + "/" + str(datetime.today().day) + " " + str(datetime.today().hour) + "時" + str(datetime.today().minute) + "分"
    task.task_type = request.form.get('task_type')
    task.priority = request.form.get('priority')
    task.title = request.form.get('title')
    task.text = request.form.get('text')
  
    db.session.add(task)
    db.session.commit()

    return redirect(url_for('.index'))



if __name__ == "__main__":
  # app.debug = True
  app.run()