from flask import g
from application.database.models import User as u
from application import auth

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = u.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = u.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True