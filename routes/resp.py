import json

def ok(http_code=200, **kw): 
    data = kw

    assert isinstance(data, dict) 
    assert isinstance(http_code, int) 

    assert not 'status' in data, 'Field \'status\' is reserved'

    data.update({'status': 'OK'})

    return json.dumps(data), http_code 

def error(http_code, error_code, message): 
    assert isinstance(http_code, int)
    assert isinstance(error_code, str)
    assert isinstance(message, str) 

    return json.dumps({
        'status': 'Error',
        'error_code': error_code,
        'message': message
    }), http_code

def error_missed_field(field_name):
    assert isinstance(field_name, str)

    return error(400, 'MISSED_FIELD', 'Missed required field: {!r}'.format(field_name))
