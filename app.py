import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from bson import ObjectId
from datetime import datetime
from controllers.user_controller import UserController
from controllers.monster_controller import MonsterController

import controllers.generate_content as GenerateContent

app = Flask(__name__)

CORS(app, methods=['GET', 'POST'], allow_headers=['Content-Type'])

userController = UserController()
monsterController = MonsterController()

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
    message_list = data["message_list"]
    last_content = data["last_content"]
    content = GenerateContent.generate_content(message_list, last_content)
    return {
        "result" : content
    }, 200

@app.route('/generate_question', methods=['post'])
def generate_question():
    data = request.get_json()
    message_list = data["message_list"]
    content = GenerateContent.generate_question(message_list)
    return {
        "result" : content
    }, 200

@app.route('/save_updated_content', methods=['post'])
def save_updated_content():
    data = request.get_json()
    message_list = data["message_list"]
    updated_content = data["updated_content"]
    res = GenerateContent.save_updated_content(message_list, updated_content )
    return {
        "result": res
    }, 200

@app.route('/hexagon_data', methods=['post'])
def get_hexagon_data():
    res = GenerateContent.get_hexagon_data()
    return {
        "result": res
    }, 200

@app.route('/create_hexagon', methods=['post'])
def create_hexagon_data():
    GenerateContent.create_hexagon_Data()
    return {
        "result": True
    }, 200

@app.route('/get/monsters', methods=['post'])
def get_monster_data():
    res = monsterController.get_monsters()
    return {
        "result": res
    }, 200

if __name__ == '__main__':
    print("Server is running on port 5000")
    app.run(debug=False)
