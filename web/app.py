from flask import Flask, jsonify
from routes import recognize

from web.routes import users

app = Flask(__name__)

app.register_blueprint(users.bp)
app.register_blueprint(recognize.bp)


def error_resp(code, msg):
    return jsonify(status='Error', error_code=code, message=msg)


def ok_resp(**data):
    assert not 'status' in data, 'Will be overwrited - data miss'

    data.update({'status': 'OK'})

    return jsonify(**data)

