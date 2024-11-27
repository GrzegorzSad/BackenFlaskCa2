from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth
from app.api.errors import success_response, error_response
from app.models import User
from flask import request

# register
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return error_response(400, message="User already exists with this email")

    # Create the new user
    user = User()
    user.from_dict(data, new_user=True)

    # Save the user in the database
    db.session.add(user)
    db.session.commit()

    # return token after successful registration
    token = user.get_token()
    db.session.commit()
    
    return success_response(201, {'token': token})


# Login
@bp.route('/login', methods=['POST'])
@basic_auth.login_required
def login():
    # Use the current user after basic auth verification
    user = basic_auth.current_user()

    # Generate and return a token
    token = user.get_token()
    db.session.commit()

    return success_response(200, {'token': token})


# Logout
@bp.route('/logout', methods=['DELETE'])
@token_auth.login_required
def logout():
    user = token_auth.current_user()

    # remove token
    user.remove_token()
    db.session.commit()

    return success_response(204)
