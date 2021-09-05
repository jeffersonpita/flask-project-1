from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from datetime import datetime

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#db = SQLAlchemy(app)
app.config['MONGODB_SETTINGS'] = {
    'db': 'flask-project-1',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

class Todo(db.Document):
    #id = db.Column(db.Integer, primary_key=True)
    content = db.StringField()
    completed = db.BooleanField(default=False)
    date_created = db.DateTimeField(default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.pk


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            new_task.save()
            return redirect('/')
        except:
            return 'There was an error'

    else:
        tasks = Todo.objects().all()
        return render_template("index.html", tasks=tasks)


@app.route('/delete/<string:id>')
def delete(id):
    task = Todo.objects.get_or_404(id=id)
    try:
        task.delete()
        return redirect('/')
    except:
        return 'There was a problem deleting'

@app.route('/update/<string:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.objects.get_or_404(id=id)

    if request.method == 'POST':
        task.update(content=request.form['content'])
        return redirect('/')
    else:
        try:
            return render_template("update.html", task=task)
        except:
            return 'Task not found'

if __name__ == '__main__':
    app.run(debug=True)
