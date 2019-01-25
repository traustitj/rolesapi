from flask import Flask
from werkzeug.contrib.cache import SimpleCache
from flask import Response
from flask import request
from server_service import Service
import json
from flask import jsonify


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    service = Service()
    return service.index()

@app.route('/user/<userid>', methods=['GET'])
def get_user(userid):
    service = Service()
    user = service.get_user_by_id(userid)
    if user is None:
        return Response("User not found", 404)
    else:
        data = user.__dict__
        return json.dumps(data)

@app.route('/role', methods=['PUT'])
def new_role():
    service = Service()
    if request.content_type == "application/json":
        role_name = request.get_json()
        role = service.new_role(role_name["name"])
        if role is None:
            return Response("Role already exists", 409)
        else:
            data = role.to_dict()
            return json.dumps(data)

    return Response("Incorrect header or data", 400)

@app.route('/role_by_id/<id>', methods=['GET'])
def get_role_by_id(id):
    service = Service()
    role = service.get_role_by_id(id)
    if role is None:
        return Response("Role not found", 404)
    data = role.to_dict()

    return json.dumps(data)

@app.route('/role_by_name/<name>', methods=['GET'])
def get_role_by_name(name):
    service = Service()
    role = service.get_role_by_name(name)
    if role is None:
        return Response("Role not found", 404)
    data = role.to_dict()

    return json.dumps(data)

@app.route('/add_user_to_role/<user_id>/<role_id>', methods=['GET'])
def add_user_to_role(user_id, role_id):
    service = Service()
    ok = service.add_user_to_role(user_id=user_id, role_id=role_id)
    if ok is True:
        role = service.get_role_by_id(role_id)
        if not role is None:
            data = role.to_dict()
            return json.dumps(data)
        
    return Response("Data not found", 404)

@app.route('/remove_user_from_role/<user_id>/<role_id>', methods=['DELETE'])
def remove_user_from_role(user_id, role_id):
    service = Service()
    ok = service.remove_user_from_role(user_id=user_id, role_id=role_id)
    if ok is True:
        role = service.get_role_by_id(role_id)
        if role is None:
            return Response("Role not found", 404)
        data = role.to_dict()
        return json.dumps(data)

@app.route('/remove_role/<role_id>', methods=["DELETE"])
def remove_role(role_id):
    service = Service()
    service.delete_role_by_id(role_id)

    return Response("", 200)

if __name__=='__main__':
    app.run(debug=False)