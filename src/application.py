from flask import Flask, Response, request
from datetime import datetime
import json
from user_information import UserInfo
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)


@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "F22-Starter-Microservice",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result


@app.route("/api/users/<id>", methods=["GET"])
def get_users_by_id(id):

    result = UserInfo.get_by_id(id)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

@app.route("/api/users/login/<email>&<pw>", methods=["GET"])
def login(email, pw):

    result = UserInfo.login(email, pw)

    rsp = Response(json.dumps(result['body']), status=result['status'], content_type="application.json")

    return rsp

@app.route("/api/users/register/<lname>&<fname>&<email>&<pw>&<phone>", methods=["POST"])
def signUp(lname, fname, email, pw, phone):

    result = UserInfo.signUp(lname, fname, email, pw, phone)

    rsp = Response(json.dumps(result['body']), status=result['status'], content_type="application.json")

    return rsp

@app.route("/api/users/<id>/<old>&<new>", methods=["PUT"])
def password(id, new, old):

    result = UserInfo.updatePassword(id, new, old)
    rsp = Response(json.dumps(result['body']), status=result['status'], content_type="application.json")
    return rsp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)

