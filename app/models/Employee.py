from typing import Optional
from datetime import datetime
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models.Department import Department

class Employee(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    ppsn: so.Mapped[str] = so.mapped_column(sa.String(16), index=True, unique=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    email: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128), index=True, unique=True)
    address: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256), index=False)
    salary: so.Mapped[Optional[float]] = so.mapped_column(sa.Numeric(8, 2))

    department_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(Department.id), index=True)
    department: so.Mapped[Optional[Department]] = so.relationship(back_populates='employees')

    # Many-to-many relationship with Project
    projects: so.Mapped[list['Project']] = so.relationship(
        'Project', secondary='employee_project', back_populates='employees', uselist=True
    )

    def __repr__(self):
        return f"<Employee {self.name}>"

    def from_dict(self, data):
        for field in ['ppsn', 'name', 'email', 'address', 'salary', 'department_id']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self, include_department=True, include_projects=True, include_salary=False):
        data = {
            'id': self.id,
            'ppsn': self.ppsn,
            'name': self.name,
            'email':self.email,
            'address': self.address,
        }
        if include_salary:
            data['salary'] = float(self.salary)
        if include_department and self.department:
            data['department'] = self.department.to_dict(include_employees=False)
        if include_projects:
            # Check if self.projects is iterable (like a list)
            if isinstance(self.projects, list):
                data['projects'] = [project.to_dict(include_employees=False) for project in self.projects]
            else:
                # If it's not a list, treat it as a single project and put it in a list
                data['projects'] = [self.projects.to_dict(include_employees=False)] if self.projects else []
        
        return data

from app.models.Project import Project