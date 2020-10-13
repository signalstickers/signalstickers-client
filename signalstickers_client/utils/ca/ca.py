"""
Handles the certificate from Signal's CA
"""

import ssl
from os.path import join, dirname

CACERT_PATH = join(dirname(__file__), 'cacert.pem')
SSL_CONTEXT = ssl.create_default_context(cafile=CACERT_PATH)
