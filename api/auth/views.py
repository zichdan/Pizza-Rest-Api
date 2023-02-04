from flask_restx import Namespace, Resource, fields
from flask import  request
from ..models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required,  get_jwt_identity
from werkzeug.exceptions import Conflict, BadRequest


auth_namespace = Namespace("auth", description="a namespace for authentication")


signup_model = auth_namespace.model(
    "Signup",{
        "id":fields.Integer(),
        "username":fields.String(required=True, description='For Username') ,
        "email":fields.String(required=True, description='For email'),
        "password":fields.String(required=True, description="For password")             
    }
)

user_model = auth_namespace.model(
    "User", {
        "id":fields.Integer(),
        "username":fields.String(required=True, description='For username'),
        "email":fields.String(required=True, description="For email"),
        "password_hash":fields.String(required=True, description="For password"),
        "is_active":fields.Boolean(description="To Check If the User is active"),
        "is_staff":fields.Boolean(description="To check if an authorized user is a staff of the company")
    }
)


login_model = auth_namespace.model(
    'Login',{
        "email":fields.String(required=True, description="Input for email"),
        "password":fields.String(required=True, description="Input for password")
    }
)



@auth_namespace.route("/signup")
class signUp(Resource):
    
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        '''
        Create a new user account
        '''
        data = request.get_json()
        
        try:
            new_user=User(
                username =data.get('username'),
                email=data.get('email'),
                password_hash=generate_password_hash(data.get('password'))
            )
            
            new_user.save()
            
            return new_user, HTTPStatus.CREATED
        except Exception as e:
             raise Conflict(f"User with emaail {data.get('email')} exists ")
        
            
    
@auth_namespace.route('/login')    
class Login(Resource):
    
    @auth_namespace.expect(login_model)
    def post(self): 
        '''
           Generate JWT token
        '''
        data = request.get_json()
            
        email = data.get('email')
        password = data.get('password')
                
        user = User.query.filter_by(email=email).first()
        
        if (email is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            
            
            response = {

                "access_token": access_token,
                'refresh_token': refresh_token
            }
            
            return response, HTTPStatus.OK
        
        raise BadRequest("Invalid Username or Password")
        
    
        
        
    
    
@auth_namespace.route('/refresh')    
class GetRefreshToken(Resource):
    
    @jwt_required(refresh=True)
    # @auth_namespace.expect(login_model)
    def post(self):
        '''
        Generate a new refresh token
        '''
        
        username = get_jwt_identity()
        
        
        access_token = create_access_token(identity=username)
        
        return {"access_token": access_token}, HTTPStatus.OK

    
@auth_namespace.route('/users')
class GetAllUsers(Resource):


    @auth_namespace.marshal_with(user_model)
    def get(self):
        '''
        Get all Users
        '''
        users = User.query.all()
        
        return users, HTTPStatus.ACCEPTED










# @auth_namespace.route('/signup')    
# class signup(Resource):

#     @auth_namespace.expect(signup_model)
#     @auth_namespace.marshal_with(user_model)
#     def post(self):
#         '''
#         Create a new user account
#         '''
#         data = request.get_json()
#         email = data.get('email')
#         check_user = User.query.filter_by(email=email).first()
#         if check_user:
#             return {'message': 'User already exists'}, HTTPStatus.CONFLICT
#         new_user=User(
#             username =data.get('username'),
#             email=data.get('email'),
#             password_hash=generate_password_hash(data.get('password'))
#         )
#         new_user.save()
#         return new_user, HTTPStatus.CREATED
    
    

# @auth_namespace.route('/login')    
# class Login(Resource):
    
#     @auth_namespace.expect(login_model)
#     def post(self): 
#         '''
#           Generate JWT token
#         '''
#         data = request.get_json()
#         email = data.get('email')
#         password = data.get('password')
#         user = User.query.filter_by(email=email).first()
#         if user is None or not check_password_hash(user.password_hash, password):
#             return {'message': 'invalid email or password'}, HTTPStatus.UNAUTHORIZED
        
#         # else:
#         #     (email is not None) and check_password_hash(user.password_hash, password)
            
#         #     access_token = create_access_token(identity=user.username)
#         #     refresh_token = create_refresh_token(identity=user.username)
        
#         # access_token = create_access_token(identity=user.username)
#         # refresh_token = create_refresh_token(identity=user.username)
#         # response = {
#         #     "access_token": access_token,
#         #     'refresh_token': refresh_token
#         # }
#         # return response, HTTPStatus.OK


    
    