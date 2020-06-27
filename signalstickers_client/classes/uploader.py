import json
import requests
import urllib3
from os import getenv
from secrets import token_hex, token_bytes
from uuid import uuid4

from signalstickers_client.classes.signalcrypto import encrypt, derive_key, decrypt
from signalstickers_client.urls import SERVICE_STICKER_FORM_URL, CDN_BASEURL
from signalstickers_client.utils.ca import CACERT_PATH


def upload_pack(pack, signal_user, signal_password):
    """
    Upload a pack, and return (pack_id, pack_key)
    """

    if not signal_user or not signal_password:
        raise RuntimeError("signal_user or signal_password not set")

    pack_key = token_hex(32)

    # Register the pack and getting authorizations
    # - "Hey, I'm {USER} and I'd like to upload {nb_stickers} stickers"
    # - "Hey, no problem, here are your credentials for uploading content"
    register_req = requests.get(SERVICE_STICKER_FORM_URL.format(
        nb_stickers=pack.nb_stickers), auth=(signal_user, signal_password), verify=CACERT_PATH)

    if register_req.status_code == 401:
        raise RuntimeError("Invalid authentication")
    if register_req.status_code == 413:
        # Yes, it comes faster than you'll expect
        raise RuntimeError(
            "Service rate limit exceeded, please try again later.")

    pack_attrs = register_req.json()

    # Encrypt the manifest
    aes_key, hmac_key = derive_key(pack_key)
    iv = token_bytes(16)

    encrypted_manifest = encrypt(
        plaintext=pack.manifest,
        aes_key=aes_key,
        hmac_key=hmac_key,
        iv=iv
    )

    # Upload the encrypted manifest
    _upload_cdn(pack_attrs["manifest"], encrypted_manifest)

    # Upload each sticker

    for sticker in pack.stickers:
        # Encrypt the sticker
        encrypted_sticker = encrypt(
            plaintext=sticker.image_data,
            aes_key=aes_key,
            hmac_key=hmac_key,
            iv=iv
        )

        _upload_cdn(pack_attrs["stickers"][sticker.id], encrypted_sticker)


    return pack_attrs["packId"], pack_key

def _upload_cdn(cdn_creds, encrypted_data):
    """
    Upload an object (manifest or sticker) to the CDN
    """

    payload = {
        'key': (None, cdn_creds["key"]),
        'x-amz-credential': (None, cdn_creds["credential"]),
        'acl': (None, cdn_creds["acl"]),
        'x-amz-algorithm': (None, cdn_creds["algorithm"]),
        'x-amz-date': (None, cdn_creds["date"]),
        'policy': (None, cdn_creds["policy"]),
        'x-amz-signature': (None, cdn_creds["signature"]),
        'Content-Type': (None, 'application/octet-stream'),
        'file': (None, encrypted_data, 'application/octet-stream'),
    }

    requests.post(CDN_BASEURL, files=payload, verify=CACERT_PATH)
