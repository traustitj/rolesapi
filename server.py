from flask import Flask
from werkzeug.contrib.cache import SimpleCache
from flask import Response
from flask import request
from server_service import Service

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    service = Service()
    return service.index()

@app.route('/user/<userid>', methods=['GET'])
def get_user(userid):
    service = Service()
    return service.get_user(userid)

@app.route('/role', methods=['PUT'])
def new_role():
    if request.content_type == "application/json":
        data = request.get_json()

        print("received data : ", data)

        return ""

    return Response("Incorrect header", 400)


if __name__=='__main__':
    app.run(debug=True)