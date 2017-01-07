import os

from flask import Blueprint, request
from logbook import Logger, FileHandler

from . import resp 
from .. import config
from .. import photo_matcher
from .models import SMS, Expense, Sale, AnalyseResult, Store, Payment


bp = Blueprint('recognize', __name__) 

log = Logger('RECOGNIZE API') 
FileHandler('/tmp/checkstar.recognize_api.log').push_application()

ERROR_RECOGNIZE_UNCERTAINTY = resp.error(http_code=400, error_code='RECOGNIZE_UNCERTAINTY', message='Image couldn\'t be precisely recognized (because bad image quality or something else).')
ERROR_MISSED_IMAGE          = resp.error(http_code=400, error_code='MISSED_IMAGE',          message='Missed required file: \'image\'')


@bp.route('/recognize/receipt', methods=['POST']) 
def recognize(): 
    file = request.files.get('image')

    if file is not None: 
        save_path = os.path.join(config.UPLOADS_DIR, file.filename)

        file.save(save_path)

        return resp.ok(receipt_data={
            'currency': 'GBP',
            'total_price': 17.24,
            'category': 'household',
            'store_name': 'My store',
            'datetime': '26-12-2016 12:31',
            'goods': [
                {
                    'name': 'HALO GU10',
                    'unit': 'items',
                    'count': 1,
                    'price': 4.0
                },
                {
                    'name': 'HALO 42W',
                    'unit': 'items',
                    'count': 1,
                    'price': 4.0
                },
                {
                    'name': 'WHITE SPIRIT',
                    'unit': 'items',
                    'count': 1,
                    'price': 2.21
                },
                {
                    'name': 'PAINT BRUSH',
                    'unit': 'items',
                    'count': 1,
                    'price': 2.05
                },
                {
                    'name': 'PRIMER',
                    'unit': 'items',
                    'count': 1,
                    'price': 4.98
                }
            ],
            'photo_url': None
        })

        if 'crop' in request.args: 
            crop = [[int(_) for _ in p_str.split('x')] for p_str in request.args['crop'].split(';')]
        else:
            crop = None

        receipt_data = photo_matcher.match(save_path, crop)

        if receipt_data is not None: 
            return resp.ok(receipt_data=receipt_data)
        else:
            return ERROR_RECOGNIZE_UNCERTAINTY
    else: 
        return ERROR_MISSED_IMAGE


@bp.route('/recognize/sms', methods=['POST']) 
def recognize_sms(): 
    sms = SMS.from_json(request.get_json(force=True, silent=True))

    log.info('SMS ({sender}): {content}'.format(**sms.__dict__))

    result = AnalyseResult(
        expenses=[
            Expense(
                name='Test expense',
                store=Store(name='restore', address=None),
                date_time='31-12-2016 12:30',
                payment=Payment(amount=30000.0, currency='RUB', type='cash'),
                category='Electronics'
            )
        ],
        sales=[
            Sale(
                name='Test sale',
                description='',
                store=Store(name='Ashan', address=None),
                region='Moscow',
                end='31-12-2017 13:40',
                link=None
            )
        ] 
    )

    return resp.ok(result=result.to_dict())
