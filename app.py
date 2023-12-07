from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timezone

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client.flask_db
todos = db.todos

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['priority']
        order = 0
        if degree == 'Important':
            order = 1
        elif degree == 'Deceptively-Important':
            order = 2
        else:
            order = 3
        complete = False 
        current_date = datetime.now(timezone.utc)
        todos.insert_one({'content': content, 'priority': degree, 'order': order, 'complete': complete, 'date': current_date}) 
        return redirect(url_for('index'))

    all_todos = todos.find().sort('order')
    return render_template('index.html', todos=all_todos) 


@app.post('/<id>/delete/')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))


@app.post('/<id>/complete/')
def complete(id):
    filter = {"_id": ObjectId(id)}
    new_values = {"$set": {"complete": True}}
    todos.update_one(filter, new_values)
    return redirect(url_for('index'))
