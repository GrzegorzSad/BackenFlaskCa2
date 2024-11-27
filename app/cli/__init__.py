from faker import Faker
from datetime import datetime
from flask import Blueprint
from app import db
from app.models import User, Employee, Department, Project, employee_project

bp = Blueprint('cli', __name__, cli_group=None)

@bp.cli.command("seed-db")
def seed_db():

    #remove my static user
    db.session.query(User).filter_by(email="test@email.com").delete()

    print("starting the seeding")

    faker = Faker("en_IE")
    num_users = 9
    num_employees = 42
    num_projects = 5
    num_departments = 4

    # Adding a user whose info you'll remember for easy login
    set_user_data = dict(
        name="test",
        email="test@email.com",
        phone='123456789',
        address='17-20 Testing Street Lower, Test Voivodship, Republic of Testingstan',
        password="password"
    )
    set_user = User()
    set_user.from_dict(set_user_data, new_user=True)
    db.session.add(set_user)
    db.session.commit()

    # users
    for _ in range(num_users):
        data = dict(
            name=faker.user_name(),
            email=faker.email(),
            phone=faker.phone_number(),
            password="password",
            address=faker.address()
        )
        user = User()
        user.from_dict(data, new_user=True)
        db.session.add(user)

    db.session.commit()  # Commit created users

    # departments
    departments = []
    for _ in range(num_departments):
        dept_data = dict(
            title=faker.company(),
            location=faker.address(),
            website=faker.url()
        )
        department = Department()
        department.from_dict(dept_data)
        db.session.add(department)
        departments.append(department)

    db.session.commit()

    # employees
    for _ in range(num_employees):
        employee_data = dict(
            ppsn=faker.ssn(),
            name=faker.name(),
            email=faker.email(),
            address=faker.address(),
            salary=faker.random_number(digits=6),
            department_id=faker.random_element([dept.id for dept in departments])
        )
        employee = Employee()
        employee.from_dict(employee_data)
        db.session.add(employee)

    db.session.commit()

    # projects
    for _ in range(num_projects):
        project_data = dict(
            title=faker.company(),
            description=faker.sentence(),
            start_date=faker.date_this_decade(),
            end_date=faker.date_this_decade()
        )
        project = Project()
        project.from_dict(project_data)
        db.session.add(project)

    db.session.commit()

    # assigning employees to projects
    employees = Employee.query.all()
    projects = Project.query.all()

    for project in projects:
        # Random number of employees to each project
        num_assigned_employees = faker.random_int(min=1, max=10)
        assigned_employees = faker.random_elements(elements=employees, length=num_assigned_employees)
        
        for employee in assigned_employees:
            # Checking if the assignment already exists in the pivot table
            existing_assignment = db.session.query(employee_project).filter_by(
                employee_id=employee.id,
                project_id=project.id
            ).first()

            if not existing_assignment:  # Only inserting if available
                db.session.execute(employee_project.insert().values(
                    employee_id=employee.id,
                    project_id=project.id
                ))

        # Add the project to the session
        db.session.add(project)

    db.session.commit()

    print("finished seeding")
