from ..models import Receipt, Store, Good


def analyse(photoPath, crop): 
    return Receipt(
        currency='GBP',
        total_price=17.24,
        category='household',
        store=Store(name="Perecrestok", address="Presnenskaya nab., 3"),
        date_time='26-12-2016 12:31',
        goods= [
            Good(
                name='HALO GU10',
                unit='items',
                count=1,
                price=4.0
            ),
            Good(
                name='HALO 42W',
                unit='items',
                count=1,
                price=4.0
            ),
            Good(
                name='WHITE SPIRIT',
                unit='items',
                count=1,
                price=2.21
            ),
            Good(
                name='PAINT BRUSH',
                unit='items',
                count=1,
                price=2.05
            ),
            Good(
                name='PRIMER',
                unit='items',
                count=1,
                price=4.98
            )
        ]
    )
