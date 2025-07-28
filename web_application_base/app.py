from flask import Flask, render_template, request, redirect, jsonify
from database.database import create_table, add_data, show_data

app = Flask(__name__)
# tasks = []

create_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    add_data(False, title)
    return redirect('/')

@app.route('/show_tasks', methods=['GET'])
def show_tasks():
    tasks = show_data()
    return jsonify(tasks)

if __name__ == '__main__':
    app.run(debug=True)