"""
Handles the certificate from Signal's CA
"""

from os.path import join, dirname

CACERT_PATH = join(dirname(__file__), 'cacert.pem')
