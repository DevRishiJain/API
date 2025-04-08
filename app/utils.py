from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def admin_required(fn):
    """Decorator to require admin access for a route"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        # Here you could check if the user has admin rights
        # For example: current_user = User.query.get(get_jwt_identity())
        # if not current_user.is_admin: return jsonify({"msg": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper

def validate_json(schema):
    """Decorator to validate incoming JSON against a schema"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return jsonify({"msg": "Missing JSON in request"}), 400
            
            data = request.get_json()
            errors = schema.validate(data)
            if errors:
                return jsonify({"msg": "Validation error", "errors": errors}), 400
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator
