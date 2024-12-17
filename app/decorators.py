from functools import wraps
from flask import request, jsonify
from sqlalchemy.orm import Session
from app.database import SessionLocal
from models import User, UserRole

def role_required(*required_roles: UserRole):
    """
    Decorator to restrict route access based on user roles.
    Args:
        *required_roles (UserRole): Roles that are allowed to access the route.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")  # Token from the request
            if not token:
                return jsonify({"error": "Unauthorized - No token provided"}), 401
            
            # Simulating user lookup from token
            db: Session = SessionLocal()
            try:
                user = db.query(User).filter(User.id == token).first()
                if not user:
                    return jsonify({"error": "Unauthorized - Invalid token"}), 401
                
                if not user.has_roles(*required_roles):
                    return jsonify({"error": "Forbidden - Insufficient permissions"}), 403
                
                # User has valid roles
                return func(*args, **kwargs)
            finally:
                db.close()
        return wrapper
    return decorator
