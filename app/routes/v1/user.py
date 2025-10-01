from flask_restx import Resource, reqparse
from flask_restx import Namespace
from app.utils.blacklist import BLACKLIST
from ...models.user import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash

user_ns = Namespace("users", description="User-related operations")

attr = reqparse.RequestParser()
attr.add_argument('name', type=str)
attr.add_argument('email', type=str, required=True, help="The field 'email' cannot be left blank")
attr.add_argument('password', type=str, required=True, help="The field 'password' cannot be left blank")

@user_ns.route("/")
class User(Resource):
    @jwt_required()
    def get(self, id):
        user = UserModel.find_user(id)
        if user: 
            return user.json()    
        return { 'message': 'User not found.' }, 404

    @jwt_required()
    def delete(self, id):
        user = UserModel.find_user(id)
        if user:
            try:
                user.delete_user()
            except:
                return { 'message': 'An interval error ocurred trying to delete user.' }, 500
            return { 'message': 'User deleted.' }
        return { 'message': 'User deleted.' }

@user_ns.route("/register/")
class UserRegister(Resource):
    def post(self):
        data = attr.parse_args()

        if UserModel.find_by_login(data['email']):
            return { "message": "The email '{}' already exists.".format(data['email']) }, 400
        
        data['password'] = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=16)

        user = UserModel(**data)

        user.save_user()
        return { 'message': 'User created successfully!' }, 201
    
@user_ns.route("/login/")
class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = attr.parse_args()

        user = UserModel.find_by_login(data['email'])

        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            return { 'access_token': access_token }, 200
        return { 'message': 'The username or password is incorrect.' }, 401
    
@user_ns.route("/logout/")
class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return { 'message': 'Logged out successfully.' }, 200