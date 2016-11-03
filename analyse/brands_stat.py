import json
from argparse import ArgumentParser


def parse_args(): 
    parser = ArgumentParser()

    modes = parser.add_subparsers(dest='mode')

    stat = modes.add_parser('stat')

    find = modes.add_parser('find')
    find.add_argument('start')

    return parser.parse_args()

def stat(data): 
    for category, items in brands.items(): 
        print('{}: {}'.format(category, len(items)))

def find(data, start): 
    for category, brands in data.items():
        for brand in brands:
            if brand.lower().startswith(start): 
                print(brand)


if __name__ == '__main__': 
    args = parse_args()

    with open('brands.json', 'r') as f: 
        brands = json.load(f)

    if args.mode == 'stat':
        stat(brands)        

    if args.mode == 'find': 
        find(brands, args.start)