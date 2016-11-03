import os
from flask import Blueprint, request, jsonify

from . import photo_matcher, config, storage, error_resp, ok_resp


bp = Blueprint('bp', __name__)

@bp.route('/recognize', methods=['POST'])
def recognize(): 
    file = request.files.get('image')

    if file is not None: 
        save_path = os.path.join(config.UPLOADS_DIR, file.filename)

        file.save(save_path)

        if 'crop' in request.args: 
            crop = [[int(_) for _ in p_str.split('x')] for p_str in request.args['crop'].split(';')]
        else:
            crop = None

        receipt_data = photo_matcher.match(save_path, crop)

        if receipt_data is not None: 
            return ok_resp(
                receipt_data=receipt_data
            ), 200
        else:
            return error_resp(
                code='RECOGNIZE_UNCERTAINTY',
                msg='Image couldn\'t be precisely recognized (because bad image quality or something else).'  
            ), 400
    else: 
        return jsonify(
            status='Error', 
            error_code='MISSED_IMAGE', 
            message='Missed required file: \'image\''
        ), 400

@bp.route('/receipts', methods=['GET', 'POST'])
def receipts(): 
    if request.method == 'GET': 
        return ok_resp(
            items=storage.get_all_receipts()
        ), 200

    elif request.method == 'POST': 
        storage.add_receipt(request.json)

        return ok_resp(), 200
