from typing import Optional
from datetime import datetime, timezone, timedelta
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import secrets


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[int] = so.mapped_column(sa.String(128), index=True, unique=True)
    phone: so.Mapped[int] = so.mapped_column(sa.String(16), index=True, unique=True)
    email: so.Mapped[int] = so.mapped_column(sa.String(128), index=True, unique=True)
    address: so.Mapped[int] = so.mapped_column(sa.String(256), index=True)
    password_hash: so.Mapped[Optional[int]] = so.mapped_column(sa.String(256))

    token: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), index=True, unique=True)
    token_expiration: so.Mapped[Optional[datetime]]

    def __repr__(self):
        return "<User {}>".format(self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_token(self, expires_in=3600):
        now = datetime.now(timezone.utc)
        if self.token and self.token_expiration.replace(tzinfo=timezone.utc) > now + timedelta(seconds=60):
            return self.token
        self.token = secrets.token_hex(16)
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token
    
    def remove_token(self):
        self.token_expiration = datetime.now(timezone.utc) - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = db.session.scalar(sa.select(User).where(User.token == token))
        if user is None or user.token_expiration.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            return None
        return user
    
    def from_dict(self, data, new_user=False):
        # Update all allowed fields
        for field in ['name', 'phone', 'email', 'address']:
            if field in data:
                setattr(self, field, data[field])
        # If it's a new user, set the password
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def to_dict(self, include_email=False, include_phone=False, include_address=False):
        data = {
            'id': self.id,
            'name': self.name,
        }
        # Include additional fields conditionally
        if include_email:
            data['email'] = self.email
        if include_phone:
            data['phone'] = self.phone
        if include_address:
            data['address'] = self.address
        return data

