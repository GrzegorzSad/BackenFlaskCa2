from app import create_app, db
from app.models import User, Employee, Department, Project, Employee_Project

import sqlalchemy.orm as so
import sqlalchemy as sa

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Department': Department, 'Employee': Employee, 'Project': Project, 'Employee_Project': Employee_Project } 