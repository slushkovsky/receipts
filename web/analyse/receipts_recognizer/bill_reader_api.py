import numpy as np
import re
import string as s


# just get 3(or set it) headlines of bill
# primitive but reliable and language-invariant way to now name of shop
# input- bill text
def get_title(bill, num_of_lines=3):
    title_lines = bill.split('\n')[:3]
    title = ''
    for line in title_lines:
        title = title + line + '\n'
    return title


# getting date as first entry of one of the following regexps
# input-bill text
def get_date(bill):
    pats = [r'([0-3][0-9]\.[0-1][0-9]\.[0-9]{1,4})',
            r'([0-3][0-9]\:[0-1][0-9]\:[0-9]{1,4})',
            r'([0-3][0-9]\-[0-1][0-9]\-[0-9]{1,4})',
            r'([0-3][0-9]\/[0-1][0-9]\/[0-9]{1,4})']
    # bill_lines=bill.split('\n')
    for pat in pats:
        search_res = re.search(pat, bill)
        if search_res != None:
            return search_res.group(1)

    return None


# getting time as first entry of a given regexp
# now used more naive regexp for time
# so for damaged time content(without ':' for example) it will not work
# input- text of bill
def get_time(bill):
    pats = [r'([0-2][0-9]\:[0-6][0-9])']
    for pat in pats:
        search_res = re.search(pat, bill)
        if search_res != None:
            return search_res.group(1)
    return None


# set text to lowercase,removing all punctuation except '.'
# input- text of bill
def clean(bill):
    bill = bill.lower()
    punct = s.punctuation
    punct = punct.replace('.', '')

    bill_clnd = ''
    for char in bill:
        if char in punct:
            continue
        bill_clnd += char
    return bill_clnd


# one hell big class for searching of goods names and prices in check
# it is supposed to be improved
class goods_extractor(object):
    def __init__(self):
        self.price_pat = r'([1-9][0-9]*\.[0-9]{2})'
        self.date_pat = r'([0-3][0-9]\.[0-1][0-9]\.[0-9]{1,4})'

    # representing good as dict with 3 fields
    def make_good(self, entry=None, price=None, content=None):
        good = {}
        good['entry'] = entry
        good['price'] = price
        good['content'] = content
        return good

    # to print goods in a handy way
    def print_good(self, good, cont=True, pr=True, ent=False):
        if ent == True:
            print('ENTRY IN BILL: ' + str(good['entry']))
        if pr == True:
            print('EXTRACTED PRICE: ' + good['price'])
        if cont == True:
            try:
                print('FIELD CONTENT:\n' + good['content'])
            except:
                print('None')

    # construct some of those dicts from bills content
    def get_raw_fields(self, bill):
        goods = []
        goods_cnt = 0
        # looking for all price-looking numbers in bill.
        for m in re.finditer(self.price_pat, bill):
            entry = m.start()
            price = m.group()
            g = self.make_good(entry, price)
            goods.append(g)
        # for every one of them(except the first)
        # collecting all stuff which is between current price and previous
        for i in range(1, len(goods)):
            from_ = goods[i - 1]['entry'] + len(goods[i - 1]['price'])
            to = goods[i]['entry']

            goods[i]['content'] = bill[from_: to]

        # for fist one we have no previous price
        # so let just take some fixed number of sting before first price
        first_entry = goods[0]['entry']
        first_lines = bill[:first_entry].split('\n')
        get_lines = 5
        if len(first_lines) > get_lines:
            content = ''
            for i in range(1, get_lines):
                content += '\n' + first_lines[-i]
            goods[0]['content'] = content

        else:
            for i in range(1, len(first_lines)):
                content += '\n' + first_lines[-i]
                goods[0]['content'] = content
            goods[0]['content'] += '\n' + first_lines[0]

        return goods

    # one general func to remove artifacts and trash goods.
    # supposed to be improved,widened,may be split to many special funcs
    # now it is removing some empty strings in fine goods content
    # and killing mistaken goods which comes from picking part of date
    # string as price
    def validate_goods(self, bill, goods):
        date_entries = []
        for m in re.finditer(self.date_pat, bill):
            entry = m.start()
            date_entries.append(entry)
        to_del = []
        for i in range(len(goods)):
            for entry in date_entries:
                if abs(entry - goods[i]['entry']) < 2:
                    to_del.append(i)

        for i in to_del:
            del goods[i]

        for good in goods:
            good['content'] = good['content'].strip()
            good['price'] = good['price'].strip()

        return goods
