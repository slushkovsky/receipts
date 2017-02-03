import json

from flask import Blueprint, request

from web.routes import near_places
from web.routes import resp


bp = Blueprint('users', __name__)


@bp.route('/users/<id>/push', methods=['POST'])
def push(id):
    service = request.json['service']
    push_id = request.json['push_id']

    return resp.ok()


@bp.route('/users/<id>/receipts', methods=['GET', 'POST'])
def receipts(id):
    if request.method == 'GET':
        return resp.ok(items=storage.receipts.get_all(id))

    elif request.method == 'POST':
        storage.receipts.add(id, **request.get_json(force=True))
        return resp.ok()


@bp.route('/users/<id>/expenses', methods=['GET', 'POST'])
def expenses(id):
    if request.method == 'GET':
        return resp.ok(items=storage.expenses.get_all())

    elif request.method == 'POST':
        storage.expenses.add(id, **request.get_json(force=True))
        return resp.ok()


@bp.route('/users/<id>/sms', methods=['POST', 'PUT'])
def sms(id):
    request_json = request.get_json(force=True, silent=True)

    if request_json is None:
        return resp.error(400, 'EMPTY_BODY', '')

    if request.method == 'POST':
        pass
        # TODO: Analyse sms history

    elif request.method == 'PUT':
        pass
        # TODO: Analyse new SMS

    # import json
    # print(json.dump(request_json, open('/home/slushkov/sms.json', 'w')))

    return resp.ok()


@bp.route('/users/<id>/location', methods=['POST'])
def location(id):
    request_json = request.get_json(force=True, silent=True)

    if request_json is None:
        request_json = {}

    try:
        lat = float(request_json['lat'])
        lng = float(request_json['lng'])
    except ValueError:
        return resp.error(400, 'BAD_FIELD_FORMAT', '')
    except KeyError as e:
        return resp.error(400, 'MISSED_FIELD',
                          'Missed required field: {}'.format(e.args[0]))

    if not (0.0 <= lat <= 90.0):
        return resp.error(400, 'BAD_COORDINATES',
                          'Bad latitude value: {}'.format(lat))

    if not (0.0 <= lng <= 180.0):
        return resp.error(400, 'BAD_COORDINATES',
                          'Bad longitude value: {}'.format(lng))

    places = near_places.find(lat, lng, names=['mcdonalds'])

    import json
    print(lat, lng)
    print(json.dumps(places))

    # TODO: send push

    return resp.ok()


@bp.route('/google_access')
def google_access():
    try:
        auth_code = request.args['code']
        state = json.loads(request.args['state'])
        id = state['id']
    except KeyError as e:
        return resp.error_missed_field(e.args[0])

    from .. import gmail

    gmail.parse(auth_code)

    return resp.ok()
