from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth
from app.api.errors import success_response, error_response
from app.models import Employee, Project
from flask import request

# create
@bp.route('/employees', methods=['POST'])
@token_auth.login_required
def employee_create():
    data = request.get_json()
    
    if Employee.query.filter_by(ppsn=data['ppsn']).first():
        return error_response(400)

    employee = Employee()
    employee.from_dict(data)

    db.session.add(employee)
    db.session.commit()

    return success_response(201, employee.to_dict())


# read
@bp.route('/employees', methods=['GET'])
@token_auth.login_required
def employees_get_all():
    employees = Employee.query.all()
    return success_response(200, [employee.to_dict() for employee in employees])


# read 1
@bp.route('/employees/<int:id>', methods=['GET'])
@token_auth.login_required
def employee_get_by_id(id):
    employee = Employee.query.get(id)
    
    if employee:
        return success_response(200, employee.to_dict())
    else:
        return error_response(404)


# update
@bp.route('/employees/<int:id>', methods=['PUT'])
@token_auth.login_required
def employee_update(id):
    data = request.get_json()
    employee = Employee.query.get(id)
    
    if not employee:
        return error_response(404)
    
    # Update employee attributes
    employee.from_dict(data)

    try:
        db.session.commit()
        return success_response(200, employee.to_dict())
    except Exception as e:
        db.session.rollback()
        return error_response(400)


# delete
@bp.route('/employees/<int:id>', methods=['DELETE'])
@token_auth.login_required
def employee_delete(id):
    employee = Employee.query.get(id)
    
    if not employee:
        return error_response(404)
    
    try:
        db.session.delete(employee)
        db.session.commit()
        return success_response(204)
    except Exception as e:
        db.session.rollback()
        return error_response(400)
