from typing import Optional
from datetime import date
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models.Employee import Employee
from typing import Optional

class Project(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(255))
    start_date: so.Mapped[Optional[date]] = so.mapped_column(sa.Date)
    end_date: so.Mapped[Optional[date]] = so.mapped_column(sa.Date)

    # Many-to-many relationship with Employee
    employees: so.Mapped[list[Employee]] = so.relationship(
        'Employee', secondary='employee_project', back_populates='projects', uselist=True
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
            # Check if self.employees is iterable (like a list)
            if isinstance(self.employees, list):
                data['employees'] = [employee.to_dict(include_department=False) for employee in self.employees]
            else:
                # If it's not a list, treat it as a single project and put it in a list
                data['employees'] = [self.projects.to_dict(include_department=False)] if self.employees else []
        
        return data
