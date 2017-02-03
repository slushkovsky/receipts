import random
from urllib.parse import urljoin
import unittest 

import requests


API_BASE_URL = 'http://a-c-b.tech'

class APITestCase(unittest.TestCase):
    def assertErrorResponse(self, resp, http_code, error_code): 
        assert isinstance(http_code, int)
        assert isinstance(error_code, str)
        assert isinstance(resp, requests.models.Response)

        self.assertEqual(resp.status_code, http_code)
        
        resp_data = resp.json()

        self.assertIn('status', resp_data)
        self.assertIn('error_code', resp_data)
        self.assertIn('message', resp_data)

        self.assertEqual(resp_data['status'], 'Error')
        self.assertEqual(resp_data['error_code'], error_code)

    def assertErrorMissedField(self, resp):
        return self.assertErrorResponse(resp, 400, 'MISSED_FIELD')

    def assertErrorBadFieldFormat(self, resp):
        return self.assertErrorResponse(resp, 400, 'BAD_FIELD_FORMAT')

    def assertOkResponse(self, resp, http_code=200):
        assert isinstance(http_code, int)
        assert isinstance(resp, requests.models.Response)

        self.assertEqual(resp.status_code, http_code)

        resp_data = resp.json()

        self.assertIn('status', resp_data)
        
        self.assertEqual(resp_data['status'], 'OK')
        

class LocationTestCase(APITestCase): 
    '''
    1) Send valid coordinates -> success
    2) Sand invalid coordinates -> error
    3) Miss all/part of fields -> error
    4) Bad filed formats -> error
    '''

    LOCATION_WITH_MCDONALDS = {'latitude': 55.687686, 'longitude': 37.603721} 
    

    def test(self):
        URL = urljoin(API_BASE_URL, '/users/{}/location'.format(random.randint(0, 100)))

        ''' 1 '''
        lat = random.uniform(0.0, 90.0)
        lng = random.uniform(0.0, 180.0)

        resp = requests.post(
            url=URL,
            json={
                'lat': lat, 
                'lng': lng
            }
        )

        self.assertOkResponse(resp)

        ''' 2 '''

        bad_points = [
            {'lat': -1.0,  'lng': 90.0 },
            {'lat': 10.0,  'lng': -5.0 },
            {'lat': -5.0,  'lng': -8.0 },
            {'lat': 100.0, 'lng': 10.0 },
            {'lat': 67.3,  'lng': 192.4}
        ]

        for bad_pnt in bad_points:
            resp = requests.post(
                url=URL,
                json={
                    'lat': bad_pnt['lat'],
                    'lng': bad_pnt['lng']
                }
            )

            self.assertErrorResponse(resp, 400, 'BAD_COORDINATES')
            
        ''' 3 ''' 
    
        self.assertErrorMissedField(requests.post(URL, json={'lat': lat}))
        self.assertErrorMissedField(requests.post(URL, json={'lng': lng}))
        self.assertErrorMissedField(requests.post(URL))
        
        ''' 4 '''

        self.assertErrorBadFieldFormat(requests.post(URL, json={'lat': 'deqdqd', 'lng': lng}))
        self.assertErrorBadFieldFormat(requests.post(URL, json={'lat': lat,      'lng': 'dwqdwqdq'}))

        

if __name__ == '__main__':
    unittest.main()



        
