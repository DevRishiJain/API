from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import db, Task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate input
    if not data or not data.get('title'):
        return jsonify({'message': 'Title is required'}), 400
    
    # Validate status if provided
    status = data.get('status', 'pending')
    if status not in ['pending', 'in-progress', 'completed']:
        return jsonify({'message': 'Invalid status value. Must be one of: pending, in-progress, completed'}), 400
    
    # Create new task
    new_task = Task(
        title=data['title'],
        description=data.get('description', ''),
        status=status,
        user_id=current_user_id
    )
    
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({
        'message': 'Task created successfully',
        'task': new_task.to_dict()
    }), 201

@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user_id = get_jwt_identity()
    
    # Optional filtering by status
    status = request.args.get('status')
    if status:
        if status not in ['pending', 'in-progress', 'completed']:
            return jsonify({'message': 'Invalid status filter'}), 400
        tasks = Task.query.filter_by(user_id=current_user_id, status=status).all()
    else:
        tasks = Task.query.filter_by(user_id=current_user_id).all()
    
    return jsonify({
        'tasks': [task.to_dict() for task in tasks],
        'count': len(tasks)
    }), 200

@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    current_user_id = get_jwt_identity()
    
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
    
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    
    return jsonify(task.to_dict()), 200

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
    
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    
    # Update task fields if provided
    if 'title' in data:
        task.title = data['title']
    
    if 'description' in data:
        task.description = data['description']
    
    if 'status' in data:
        if data['status'] not in ['pending', 'in-progress', 'completed']:
            return jsonify({'message': 'Invalid status value. Must be one of: pending, in-progress, completed'}), 400
        task.status = data['status']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Task updated successfully',
        'task': task.to_dict()
    }), 200

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user_id = get_jwt_identity()
    
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
    
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({
        'message': 'Task deleted successfully'
    }), 200
