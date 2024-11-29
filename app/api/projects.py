from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth
from app.api.errors import success_response, error_response
from app.models import Project, Employee
from flask import request

# Create
@bp.route('/projects', methods=['POST'])
@token_auth.login_required
def project_create():
    data = request.get_json()
    
    if Project.query.filter_by(name=data['name']).first():
        return error_response(400)

    project = Project()
    project.from_dict(data)

    db.session.add(project)
    db.session.commit()

    return success_response(201, project.to_dict())


# Read
@bp.route('/projects', methods=['GET'])
@token_auth.login_required
def projects_get_all():
    projects = Project.query.all()
    return success_response(200, [project.to_dict() for project in projects])


# Read 1
@bp.route('/projects/<int:id>', methods=['GET'])
@token_auth.login_required
def project_get_by_id(id):
    project = Project.query.get(id)
    
    if project:
        return success_response(200, project.to_dict())
    else:
        return error_response(404)


# Update
@bp.route('/projects/<int:id>', methods=['PUT'])
@token_auth.login_required
def project_update(id):
    data = request.get_json()
    project = Project.query.get(id)
    
    if not project:
        return error_response(404)
    
    project.from_dict(data)

    try:
        db.session.commit()
        return success_response(200, project.to_dict())
    except Exception as e:
        db.session.rollback()
        return error_response(400)


# Delete
@bp.route('/projects/<int:id>', methods=['DELETE'])
@token_auth.login_required
def project_delete(id):
    project = Project.query.get(id)
    
    if not project:
        return error_response(404)
    
    try:
        db.session.delete(project)
        db.session.commit()
        return success_response(204)
    except Exception as e:
        db.session.rollback()
        return error_response(400)
    
# Add employees to a project
@bp.route('/projects/<int:project_id>/employees', methods=['POST'])
@token_auth.login_required
def add_employees_to_project(project_id):
    project = Project.query.get(project_id)
    if not project:
        return error_response(404)

    data = request.get_json()
    employee_ids = data.get('employee_ids', [])

    if not isinstance(employee_ids, list) or not employee_ids:
        return error_response(400)

    employees = Employee.query.filter(Employee.id.in_(employee_ids)).all()

    if not employees:
        return error_response(404)

    # Add employees to the project's relationship
    for employee in employees:
        if employee not in project.employees:
            project.employees.append(employee)

    print(project.employees, 'project.employees')
    try:
        db.session.commit()
        return success_response(200, message="employees added to project")
    except Exception as e:
        db.session.rollback()
        print('111')
        return error_response(400)

# remove Employees from a project
@bp.route('/projects/<int:project_id>/employees', methods=['DELETE'])
@token_auth.login_required
def remove_employees_from_project(project_id):
    project = Project.query.get(project_id)
    if not project:
        return error_response(404)

    data = request.get_json()
    employee_ids = data.get('employee_ids', [])

    if not isinstance(employee_ids, list) or not employee_ids:
        return error_response(400)

    employees = Employee.query.filter(Employee.id.in_(employee_ids)).all()

    if not employees:
        return error_response(404)

    # Remove employees from the project's relationship
    for employee in employees:
        if employee in project.employees:
            project.employees.remove(employee)

    try:
        db.session.commit()
        return success_response(200, message="employees removed from project")
    except Exception as e:
        db.session.rollback()
        return error_response(400)
