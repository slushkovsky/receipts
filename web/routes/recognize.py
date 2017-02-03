import os

from flask import Blueprint, request
from logbook import Logger, FileHandler

from web.models import SMS
from web.routes import resp
from web import config
from web.analyse.receipt import analyse as reciept_analyse
from web.analyse.sms import analyse as sms_analyse
from web.analyse.gmail import analyse as gmail_analyse


bp = Blueprint('recognize', __name__)

log = Logger('RECOGNIZE API') 
FileHandler('/tmp/checkstar.recognize_api.log').push_application()

ERROR_RECOGNIZE_UNCERTAINTY = resp.error(http_code=400, error_code='RECOGNIZE_UNCERTAINTY', message='Image couldn\'t be precisely recognized (because bad image quality or something else).')
ERROR_MISSED_IMAGE          = resp.error(http_code=400, error_code='MISSED_IMAGE', message='Missed required file: \'image\'')


@bp.route('/recognize/receipt', methods=['POST']) 
def recognize(): 
    file = request.files.get('image')

    if file is not None: 
        save_path = os.path.join(config.UPLOADS_DIR, file.filename)

        file.save(save_path)

        if 'crop' in request.args: 
            crop = [[int(_) for _ in p_str.split('x')] for p_str in request.args['crop'].split(';')]
        else:
            crop = None

        receipt = reciept_analyse(save_path, crop)

        return resp.ok(result=receipt.to_dict())
    else: 
        return ERROR_MISSED_IMAGE


@bp.route('/recognize/sms', methods=['POST']) 
def recognize_sms(): 
    sms = SMS.from_json(request.get_json(force=True, silent=True))

    log.info('SMS ({sender}): {content}'.format(**sms.__dict__))

    return resp.ok(result=sms_analyse(sms).to_dict())


@bp.route('/recognize/gmail', methods=['POST']) 
def recognize_gmail():
    auth_code = request.get_json(force=True, silent=True)['auth_code']

    return resp.ok(result=gmail_analyse(auth_code).to_dict())
