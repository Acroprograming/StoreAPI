from models.user import UserModel
from flask_jwt import JWT

def authenticate(username,password):
    user=UserModel.find_by_username(username)
    if user and password==user.password:
        return user

def identity(payload):
    user_id=payload["identity"]
    return UserModel.find_by_Id(user_id)

