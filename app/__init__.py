from flask import Flask, render_template, jsonify, request
from .scheduler.scheduler import Scheduler
from .models.resource import Resource
from .models.task import Task

app = Flask(__name__)
scheduler = Scheduler()

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/tasks')
def tasks():
    return render_template('tasks.html')

@app.route('/api/resources', methods=['POST'])
def add_resource():
    data = request.json
    resource = Resource(
        id=len(scheduler.resources),
        cpu_cores=float(data['cpu_cores']),
        memory_gb=float(data['memory_gb'])
    )
    scheduler.add_resource(resource)
    return jsonify({'status': 'success'})

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    task = Task(
        id=len(scheduler.task_queue),
        priority=int(data['priority']),
        deadline=float(data['deadline']),
        required_cpu=float(data['required_cpu']),
        required_memory=float(data['required_memory'])
    )
    scheduler.add_task(task)
    return jsonify({'status': 'success'})

@app.route('/api/metrics')
def get_metrics():
    metrics = {
        'cpu_utilization': [],
        'memory_utilization': [],
        'resources': []
    }
    
    for resource in scheduler.resources:
        cpu_util = (resource.total_cpu - resource.available_cpu) / resource.total_cpu * 100
        mem_util = (resource.total_memory - resource.available_memory) / resource.total_memory * 100
        
        metrics['cpu_utilization'].append(cpu_util)
        metrics['memory_utilization'].append(mem_util)
        
        # Add detailed resource information
        metrics['resources'].append({
            'total_cpu': resource.total_cpu,
            'available_cpu': resource.available_cpu,
            'total_memory': resource.total_memory,
            'available_memory': resource.available_memory
        })
    
    return jsonify(metrics)

def create_app():
    scheduler.start()
    return app 