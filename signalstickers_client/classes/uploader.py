import json
from os import getenv
from secrets import token_hex, token_bytes
from uuid import uuid4

import anyio
import asks

from signalstickers_client.classes.signalcrypto import encrypt, derive_key, decrypt
from signalstickers_client.urls import SERVICE_STICKER_FORM_URL, CDN_BASEURL
from signalstickers_client.utils.ca import SSL_CONTEXT


async def upload_pack(pack, signal_user, signal_password):
    """
    Upload a pack, and return (pack_id, pack_key)
    """

    if not signal_user or not signal_password:
        raise RuntimeError("signal_user or signal_password not set")

    pack_key = token_hex(32)

    # Register the pack and getting authorizations
    # - "Hey, I'm {USER} and I'd like to upload {nb_stickers} stickers"
    # - "Hey, no problem, here are your credentials for uploading content"
    register_req = await asks.get(SERVICE_STICKER_FORM_URL.format(
        nb_stickers=pack.nb_stickers_with_cover),
        auth=asks.BasicAuth((signal_user, signal_password)),
        ssl_context=SSL_CONTEXT,
    )

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
    await _upload_cdn(pack_attrs["manifest"], encrypted_manifest)

    # Upload each sticker
    stickers_list = pack.stickers

    if pack.cover:
        stickers_list.append(pack.cover)

    async with anyio.create_task_group() as tg:
	    for sticker in stickers_list:
	        # Encrypt the sticker
	        encrypted_sticker = encrypt(
	            plaintext=sticker.image_data,
	            aes_key=aes_key,
	            hmac_key=hmac_key,
	            iv=iv
	        )

	        await tg.spawn(_upload_cdn, pack_attrs["stickers"][sticker.id], encrypted_sticker)

    return pack_attrs["packId"], pack_key

async def _upload_cdn(cdn_creds, encrypted_data):
    """
    Upload an object (manifest or sticker) to the CDN
    """

    payload = {
        'key': cdn_creds["key"],
        'x-amz-credential': cdn_creds["credential"],
        'acl': cdn_creds["acl"],
        'x-amz-algorithm': cdn_creds["algorithm"],
        'x-amz-date': cdn_creds["date"],
        'policy': cdn_creds["policy"],
        'x-amz-signature': cdn_creds["signature"],
        'Content-Type': 'application/octet-stream',
        'file': encrypted_data,
    }

    await asks.post(CDN_BASEURL, multipart=payload, ssl_context=SSL_CONTEXT)
