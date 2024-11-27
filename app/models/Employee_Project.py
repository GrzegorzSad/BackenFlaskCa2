import sqlalchemy as sa
from app import db

# many to many
employee_project = sa.Table(
    'employee_project',
    db.metadata,
    sa.Column('employee_id', sa.Integer, sa.ForeignKey('employee.id'), primary_key=True),
    sa.Column('project_id', sa.Integer, sa.ForeignKey('project.id'), primary_key=True)
)
