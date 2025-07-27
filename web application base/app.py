from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)
tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    tasks.append({"id": len(tasks)+1, "title": title, "done": False})
    return redirect('/')

@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['done'] = not task['done']
            break
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)