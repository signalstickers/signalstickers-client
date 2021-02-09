from secrets import token_hex, token_bytes

import anyio

from signalstickers_client.classes.signalcrypto import encrypt, derive_key
from signalstickers_client.urls import SERVICE_STICKER_FORM_URL, CDN_BASEURL
from signalstickers_client.errors import HTTPException, Unauthorized, RateLimited


async def upload_pack(http, pack, signal_user, signal_password):
    """
    Upload a pack, and return (pack_id, pack_key)
    """

    if not signal_user or not signal_password:
        raise ValueError("signal_user or signal_password not set")

    pack_key = token_hex(32)

    # Register the pack and getting authorizations
    # - "Hey, I'm {USER} and I'd like to upload {nb_stickers} stickers"
    # - "Hey, no problem, here are your credentials for uploading content"
    register_resp = await http.get(SERVICE_STICKER_FORM_URL.format(
        nb_stickers=pack.nb_stickers_with_cover),
        auth=(signal_user, signal_password),
        timeout=None,
    )

    if register_resp.status_code == 401:
        raise Unauthorized(register_resp, "Invalid authentication")
    if register_resp.status_code == 413:
        # Yes, it comes faster than you'll expect
        raise RateLimited(
            register_resp, "Service rate limit exceeded, please try again later.")
    if register_resp.status_code not in range(200, 300):
        raise HTTPException(register_resp, "Unhandled HTTP exception while trying to upload a pack")

    pack_attrs = register_resp.json()

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
    await _upload_cdn(http, pack_attrs["manifest"], encrypted_manifest)

    # Upload each sticker
    stickers_list = pack.stickers

    if pack.cover:
        stickers_list.append(pack.cover)

    # upload 5 stickers at a time in parallel
    for i in range(0, len(stickers_list), 5):
        async with anyio.create_task_group() as tg:
            for sticker in stickers_list[i:i+5]:
                # Encrypt the sticker
                encrypted_sticker = encrypt(
                    plaintext=sticker.image_data,
                    aes_key=aes_key,
                    hmac_key=hmac_key,
                    iv=iv
                )

                await tg.spawn(_upload_cdn, http, pack_attrs["stickers"][sticker.id], encrypted_sticker)

    return pack_attrs["packId"], pack_key

async def _upload_cdn(http, cdn_creds, encrypted_data):
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

    upload_resp = await http.post(CDN_BASEURL, files=payload, timeout=None)
    if upload_resp.status_code not in range(200, 300):
        raise HTTPException(upload_resp, "Unhandled HTTP exception while trying to upload to the sticker CDN")
