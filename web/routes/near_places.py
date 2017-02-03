import os
import json
import time
import requests

API_KEY = 'AIzaSyDfSq5SZfHHUppf69Oc2sjCwTw1mbnX6Ww'


def find(lat, lng, radius=100, names=[]):
    assert isinstance(lat, float), 'Latitude must be a float value'
    assert isinstance(lng, float), 'Longitude must be a float value'
    assert isinstance(radius, int), 'Search radius must be an integer'
    assert isinstance(names, list), 'Names parameter must be a list'

    req_params = {
        'key': API_KEY,
        'location': '{},{}'.format(lat, lng),
        'radius': radius,
        'name': ' '.join(names)
    }

    places = []
    next_page_token = None

    while True:
        if next_page_token is not None:
            req_params.update({'pagetoken': next_page_token})

        resp = requests.get(
            'https://maps.googleapis.com/maps/api/place/nearbysearch/json',
            params=req_params).json()

        if resp['status'] == 'ZERO_RESULTS':
            break

        assert resp['status'] == 'OK', resp

        places.append(resp['results'])

        next_page_token = resp.get('next_page_token')

        if next_page_token is None:
            break

        time.sleep(2)

    return places
