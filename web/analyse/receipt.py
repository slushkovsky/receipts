from dateutil.parser import parse

from web.models import Receipt, Store, Good

from .receipts_recognizer.bill_reader import recognize


def analyse(photoPath, crop):
    result = recognize(photoPath)

    total_price = sum(
        (float(g['price']) for g in result['goods'])
    )
    return Receipt(
        currency='RUB',
        total_price=total_price,
        category='household',
        store=Store(name=result['title'], address=''),
        date_time=parse(
            '{} {}'.format(result['date'], result['time'])
        ).strftime('%d-%m-%Y %H:%M'),
        goods=[
            Good(
                name=g['content'], unit='items',
                count=int(g['entry']), price=float(g['price'])
            ) for g in result['goods']
        ]
    )

    # return Receipt(
    #     currency='GBP',
    #     total_price=17.24,
    #     category='household',
    #     store=Store(name="Perecrestok", address="Presnenskaya nab., 3"),
    #     date_time='26-12-2016 12:31',
    #     goods=[
    #         Good(
    #             name='HALO GU10',
    #             unit='items',
    #             count=1,
    #             price=4.0
    #         ),
    #         Good(
    #             name='HALO 42W',
    #             unit='items',
    #             count=1,
    #             price=4.0
    #         ),
    #         Good(
    #             name='WHITE SPIRIT',
    #             unit='items',
    #             count=1,
    #             price=2.21
    #         ),
    #         Good(
    #             name='PAINT BRUSH',
    #             unit='items',
    #             count=1,
    #             price=2.05
    #         ),
    #         Good(
    #             name='PRIMER',
    #             unit='items',
    #             count=1,
    #             price=4.98
    #         )
    #     ]
    # )
