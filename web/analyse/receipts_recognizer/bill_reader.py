#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import sys

from googleapiclient import discovery
from googleapiclient import errors

from . import bill_reader_api as br
from .checkstart_credentials import GOOGLE_CREDENTIALS

DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'  # noqa
BATCH_SIZE = 10


class VisionApi:
    """Construct and use the Google Vision API service."""

    def __init__(self, api_discovery_file='vision_api.json'):
        self.credentials = GOOGLE_CREDENTIALS
        self.service = discovery.build(
            'vision', 'v1', credentials=self.credentials,
            discoveryServiceUrl=DISCOVERY_URL
        )

    def detect_text(self, input_filenames, num_retries=3, max_results=6):
        """Uses the Vision API to detect text in the given file.
        """
        images = {}
        for filename in input_filenames:
            with open(filename, 'rb') as image_file:
                images[filename] = image_file.read()

        batch_request = []
        for filename in images:
            batch_request.append({
                'image': {
                    'content': base64.b64encode(
                        images[filename]).decode('UTF-8')
                },
                'features': [{
                    'type': 'TEXT_DETECTION',
                    'maxResults': max_results,
                }],
                "imageContext": {
                    "languageHints": ['ru', 'en'],
                },
            })
        request = self.service.images().annotate(
            body={'requests': batch_request}
        )

        try:
            responses = request.execute(num_retries=num_retries)
            if 'responses' not in responses:
                return {}
            text_response = {}
            for filename, response in zip(images, responses['responses']):
                if 'error' in response:
                    print("API Error for %s: %s" % (
                        filename,
                        response['error']['message']
                        if 'message' in response['error']
                        else ''))
                    continue
                if 'textAnnotations' in response:
                    text_response[filename] = response['textAnnotations']
                else:
                    text_response[filename] = []
            return text_response
        except errors.HttpError as e:
            print("Http Error for %s: %s" % (filename, e))
        except KeyError as e2:
            print("Key error: %s" % e2)


def get_content(response):
    blocks_names = response.keys()
    field_name = u'description'
    blocks_cont = [response[i][0][field_name] for i in blocks_names]

    return blocks_cont


def recognize(file_name):
    from itertools import takewhile

    # class amount_predictor_including:
    #     def __init__(self):
    #         self._amount_meeted = False
    #
    #     def __call__(self, item):
    #         if self._amount_meeted:
    #             return False
    #         if item['content'] == 'итог':
    #             self._amount_meeted = True
    #             return True
    #         else:
    #             return True

    ge = br.goods_extractor()
    vis_api = VisionApi()

    resp = vis_api.detect_text([file_name])
    conts = get_content(resp)
    b = conts[0]

    # delete odd punctuation and convert to lowecase
    bill_clnd = br.clean(b)

    # get all goods conten as list of good dicts(read more in api file)
    goods = ge.get_raw_fields(bill_clnd)
    # clean them
    goods = ge.validate_goods(bill_clnd, goods)

    # extract time,date,title from bill content
    time = br.get_time(b)
    date = br.get_date(b)
    title = br.get_title(b)

    return {
        'time': time,
        'date': date,
        'title': title,
        'goods': list(
            takewhile(
                lambda i: i['content'] != 'итог', goods
            )
        )
    }

    # return {
    #     'time': time,
    #     'date': date,
    #     'title': title,
    #     'goods': list(
    #         takewhile(
    #             amount_predictor_including(), goods
    #         )  # skip until meet amount statement, but keep it in results using
    #     )      # amount_predictor_including .
    # }          # Stupid solution, but u know better?


def main():
    ge = br.goods_extractor()
    vis_api = VisionApi()
    if len(sys.argv) > 1:
        file_name = [sys.argv[1]]
        # file_name=['test_img/5.jpg','test_img/eng_bill.jpg']
        print(file_name)
        response = vis_api.detect_text(file_name)
        contents = get_content(response)
        bill = contents[0]

        # delete odd punctuation and convert to lowecase
        bill_clnd = br.clean(bill)

        # get all goods conten as list of good dicts(read more in api file)
        goods = ge.get_raw_fields(bill_clnd)
        # clean them
        goods = ge.validate_goods(bill_clnd, goods)

        # extract time,date,title from bill content
        time = br.get_time(bill)
        date = br.get_date(bill)
        title = br.get_title(bill)

        time = 'Time: ' + time + '\n'
        date = 'Date: ' + date + '\n'
        title = 'Title:\n' + title + '\n'
        print(title)
        print(date)
        print(time)
        for good in goods:
            print('Field content:\n' + good['content'])
            print('Price:' + good['price'] + '\n')
        '''
        with open('content.txt','w') as f:
            f.write(title.decode('utf8'))
            f.write(date.decode('utf8'))
            f.write(time.decode('utf8'))

            for good in goods:
                f.write('Field content:\n'+str(good['content']))
                f.write('Price:' +str(good['price']))

        with open('original.txt','w') as o:
            o.write(bill)
        '''

if __name__ == '__main__':
    main()
