import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db 
from typing import Optional

class Department(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(128), unique=True, index=True)
    location: so.Mapped[str] = so.mapped_column(sa.String(128), index=False)
    website: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256), index=False)

    employees: so.WriteOnlyMapped['Employee'] = so.relationship(back_populates='department')

    def __repr__(self):
        return f"<Department {self.title}>"

    def from_dict(self, data):
        for field in ['title', 'location', 'website']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self, include_employees=True):
        data = {
            'id': self.id,
            'title': self.title,
            'location': self.location,
            'website': self.website,
        }
        if include_employees:
            data['employees'] = [employee.to_dict(include_department=False) for employee in self.employees]
        return data

from app.models.Employee import Employee