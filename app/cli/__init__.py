from faker import Faker
from datetime import timezone

from flask import Blueprint

bp = Blueprint('cli', __name__, cli_group=None)

from app import db
from app.models import User

@bp.cli.command("seed-db")
def seed_db():
    faker = Faker("en_IE")
    num_users = 9

    #adding a user whoose info ill remember
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


    for _ in range(num_users):
        data = dict(
            name = faker.user_name(),
            email = faker.email(),
            phone = faker.phone_number(),
            password = "password",
            address = faker.address()
        )
        user = User()
        user.from_dict(data, new_user = True)
        db.session.add(user)

        db.session.commit()