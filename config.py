import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

UPLOADS_DIR = '/tmp'
DB_URI = 'sqlite:////tmp/receipts.db'
PRESETS_DIR = os.path.join(SCRIPT_DIR, 'presets')