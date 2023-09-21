from dotenv import dotenv_values

import jwt
import datetime

from models.users import Users

env_vars = dotenv_values('.env')

TOKEN_EXPIRE = 600 # 10 minutes

class UserController(object):
    # Init MongoDB and create colection
    user_model = None

    def __init__(self) -> None:
        self.user_model = Users()

    def signup(self, data):
        user_name = data['name']
        user_email = data['email']
        user_password = data['password']
        user_type = data['type']


        user_item = {
            "name": user_name,
            "email": user_email,
            "password": user_password,
            "type": user_type
        }

        result = self.user_model.find_one({"email": user_email, "password": user_password})

        if result is not None:
            return "User created", False
        else:
            self.user_model.create(user_item)
            token = jwt.encode({"username": user_item["name"], "email" : user_item["email"], 
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRE)}, env_vars["SECRET_KEY"], algorithm='HS256')
            return token, True
    
    def login(self, data):
        user_email = data['email']
        user_password = data['password']
        user_type = data['type']

        result = self.user_model.find_one({"email": user_email, "password": user_password, "type": user_type})
        if result is not None:
            token = jwt.encode({"username": result["name"], "email" : result["email"], 
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRE)}, env_vars["SECRET_KEY"], algorithm='HS256')
            return token, True
        else:
            return None, False
