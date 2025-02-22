from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask App
app = Flask(__name__)

# Database Configuration (Use an environment variable for testing)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = False  # This can be set to True in tests

db = SQLAlchemy(app)

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Create database tables
def init_db():
    with app.app_context():
        db.create_all()

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health_check():
    return jsonify({'status': 'UP'})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify({'tasks': [{'id': task.id, 'title': task.title, 'completed': task.completed} for task in tasks]})

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return jsonify({'id': task.id, 'title': task.title, 'completed': task.completed})
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    task = Task(title=data['title'])
    db.session.add(task)
    db.session.commit()
    return jsonify({'id': task.id, 'title': task.title, 'completed': task.completed}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify({'id': task.id, 'title': task.title, 'completed': task.completed})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 200


# @app.route('/check-db')
# def check_db():
#     tables = db.engine.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
#     return jsonify({'tables': [table[0] for table in tables]})


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
