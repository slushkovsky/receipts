from flask import Flask, jsonify

from . import config

app = Flask(__name__)

def error_resp(code, msg): 
	return jsonify(status='Error', error_code=code, message=msg)

def ok_resp(**data): 
	assert not 'status' in data, 'Will be overwrited - data miss'

	data.update({'status': 'OK'})

	return jsonify(**data)

from . import routes
