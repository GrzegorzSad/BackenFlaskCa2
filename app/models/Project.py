from typing import Optional
from datetime import date
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models.Employee import Employee

class Project(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(255))
    start_date: so.Mapped[date] = so.mapped_column(sa.Date)
    end_date: so.Mapped[date] = so.mapped_column(sa.Date)

    # Many-to-many relationship with Employee
    employees: so.Mapped[Employee] = so.relationship(
        'Employee', secondary='employee_project', back_populates='projects'
    )

    def __repr__(self):
        return f"<Project {self.title}>"

    def from_dict(self, data):
        for field in ['title', 'description', 'start_date', 'end_date']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self, include_dates=True, include_employees=True):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }
        if include_dates:
            data['start_date'] = self.start_date.isoformat()
            data['end_date'] = self.end_date.isoformat()
        if include_employees:
            data['employees'] = [employee.to_dict(include_department=False) for employee in self.employees]


        return data
