from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'tasks.json')

def read_tasks():
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def write_tasks(tasks):
    with open(DATA_FILE, 'w') as file:
        json.dump(tasks, file, indent=2)

@app.route('/api/tasks', methods=['GET'])
def get_all_tasks():
    try:
        return jsonify(read_tasks())
    except Exception as e:
        return jsonify({"error": "Failed to read tasks", "details": str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_single_task(task_id):
    try:
        tasks = read_tasks()
        task = next((t for t in tasks if t['id'] == task_id), None)
        if task:
            return jsonify(task)
        return jsonify({"error": f"Task with ID {task_id} not found"}), 404
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task_status(task_id):
    try:
        tasks = read_tasks()
        task = next((t for t in tasks if t['id'] == task_id), None)
        
        if not task:
            return jsonify({"error": f"Task with ID {task_id} not found"}), 404
            
        data = request.get_json()
        if data and 'status' in data:
            task['status'] = data['status']
            write_tasks(tasks)
            
        return jsonify({"message": "Task updated successfully", "task": task})
    except Exception as e:
        return jsonify({"error": "Failed to update task", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
