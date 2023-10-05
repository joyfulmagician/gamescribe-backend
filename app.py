import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from bson import ObjectId
from datetime import datetime
from controllers.user_controller import UserController

import controllers.generate_content as GenerateContent

app = Flask(__name__)

CORS(app, methods=['GET', 'POST'], allow_headers=['Content-Type'])

userController = UserController()

# Encodeing the ObjectID and datetime fields as a JSON string
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId) or isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route('/', methods=['post'])
def get_request():
    return "Good", 200

@app.route('/signup', methods=['post'])
def signup_user():
    # Access the request data
    data = request.get_json()
    
    token, res = userController.signup(data)

    if res == True:
        return jsonify({"status" : True, "token" : token}), 200
    else:
        return jsonify({"status" : False, "result" : token }), 200

@app.route('/login', methods=['post'])
def login_user():
    data = request.get_json()

    token, res = userController.login(data)
    
    if res:
        return jsonify({"status" : True, "token" : token}), 200
    else:
        return jsonify({"status" : False, "result" : token}), 200
    
@app.route('/generate_content', methods=['post'])
def generate_content():
    data = request.get_json()
    user_input = data["user_input"]
    content = GenerateContent.generate_content(user_input)
    return {
        "result" : content
    }, 200

if __name__ == '__main__':
    print("Server is running on port 5000")
    app.run(debug=False)
