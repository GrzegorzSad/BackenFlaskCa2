from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth
from app.api.errors import success_response, error_response
from app.models import Department
from flask import request

# Create
@bp.route('/departments', methods=['POST'])
@token_auth.login_required
def department_create():
    data = request.get_json()
    
    if Department.query.filter_by(title=data['title']).first():
        return error_response(400)

    department = Department()
    department.from_dict(data)

    db.session.add(department)
    db.session.commit()

    return success_response(201, department.to_dict())


# Read
@bp.route('/departments', methods=['GET'])
@token_auth.login_required
def departments_get_all():
    departments = Department.query.all()
    return success_response(200, [department.to_dict() for department in departments])


# Read 1
@bp.route('/departments/<int:id>', methods=['GET'])
@token_auth.login_required
def department_get_by_id(id):
    department = Department.query.get(id)
    
    if department:
        return success_response(200, department.to_dict())
    else:
        return error_response(404)


# Update
@bp.route('/departments/<int:id>', methods=['PUT'])
@token_auth.login_required
def department_update(id):
    data = request.get_json()
    department = Department.query.get(id)
    
    if not department:
        return error_response(404)
    
    department.from_dict(data)

    try:
        db.session.commit()
        return success_response(200, department.to_dict())
    except Exception as e:
        db.session.rollback()
        return error_response(400)


# Delete
@bp.route('/departments/<int:id>', methods=['DELETE'])
@token_auth.login_required
def department_delete(id):
    department = Department.query.get(id)
    
    if not department:
        return error_response(404)
    
    try:
        db.session.delete(department)
        db.session.commit()
        return success_response(204)
    except Exception as e:
        db.session.rollback()
        return error_response(400)
