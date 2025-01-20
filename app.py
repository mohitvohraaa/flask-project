import os
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///MyTodo.db"

db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    Title=db.Column(db.String(150),nullable=False)
    desc=db.Column(db.String(450),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self)->str:
        return f"{self.sno}-{self.title}"



@app.route("/",methods=['GET','POST'])
def hello_world():
    if request.method=="POST":
        title=request.form['Title']
        desc=request.form['desc']
        todo=Todo(Title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo=Todo.query.all()
    return render_template('index.html',alltodo=alltodo)
    #return "<p>Hello, World!</p>"
@app.route("/products")
def products():
    return "this is produxcts page"
@app.route("/delete/<int:SNo>")
def delete(SNo):
    todo=Todo.query.filter_by(sno=SNo).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
@app.route("/update/<int:SNo>", methods=["GET", "post"])
def update(SNo):
    todo = Todo.query.filter_by(sno=SNo).first()
    if request.method == 'POST':
        # Get updated values from the form
        title = request.form['Title']
        desc = request.form['desc']

        # Update the todo item
        todo.Title = title
        todo.desc = desc
        db.session.commit()

        return redirect("/")
    return render_template('update.html', todo=todo)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Default to port 5000 for local development
    app.run(host="0.0.0.0", port=port)

