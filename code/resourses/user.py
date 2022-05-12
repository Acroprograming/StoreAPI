from flask_restful import Resource, reqparse
from blocklist import BLOCKLIST
from models.user import UserModel
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,get_jwt_identity,get_jwt)

_user_parser=reqparse.RequestParser()
_user_parser.add_argument("username",help="username is required",required=True,type=str)
_user_parser.add_argument("password",help="password is required",required=True,type=str)
class UserRegister(Resource):
    
    def post(self):
        data=_user_parser.parse_args()
        if UserModel.find_by_username(data["username"]):
            return {"message":"username already exists"}
        
        user=UserModel(**data)
        user.save_to_db()
        return {"message":"user created successfully"}, 201
        
class User(Resource):
    def get(cls,user_id):
        user=UserModel.find_by_Id(user_id)
        if(user):
            return user.json()
        return {"message":"User does not exist"}, 404
    def delete(cls,user_id):
        user=UserModel.find_by_Id(user_id)
        if(user):
            user.delete_from_db()
            return {"message":"User deleted successfully"}
        return {"message":"User does not exist"}, 404

        
class UserLogin(Resource):
    @classmethod
    def post(cls):
        data=_user_parser.parse_args()
        user=UserModel.find_by_username(data["username"])
        if user and data["password"]==user.password:
            access_token=create_access_token(identity=user.id,fresh=True)
            refresh_token=create_refresh_token(user.id)
            return {
                "access_token":access_token,
                "refresh_token":refresh_token
            },200
        return {"message":"Invalid Credentials"},401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti=get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message":"User successfully logged out"}

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user=get_jwt_identity()
        new_token=create_access_token(identity=current_user,fresh=False)
        return {'access_token':new_token},200