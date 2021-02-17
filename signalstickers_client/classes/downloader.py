"""
This module allows to get full sticker packs, contains both data and metadata
"""

import anyio
import httpx
from signalstickers_client.models.sticker import Sticker
from signalstickers_client.models.sticker_pack import StickerPack
from signalstickers_client.urls import CDN_MANIFEST_URL, CDN_STICKER_URL
from signalstickers_client.classes.signalcrypto import decrypt
from signalstickers_client.classes.Stickers_pb2 import Pack
from signalstickers_client.errors import HTTPException, NotFound


async def get_pack(http: httpx.AsyncClient, pack_id, pack_key):
    """
    Return a `StickerPack` and all of its enclosing `Sticker` images from its id and key
    """
    pack = await get_pack_metadata(http, pack_id, pack_key)

    async def get_sticker_image(sticker):
        sticker.image_data = await get_sticker(http, sticker.id, pack_id, pack_key)

    async with anyio.create_task_group() as tg:
        # The StickerPack object is created, but stickers and cover
        # are still missing the raw_image
        await tg.spawn(get_sticker_image, pack.cover)
        for sticker in pack.stickers:
            await tg.spawn(get_sticker_image, sticker)

    return pack


async def get_pack_metadata(http, pack_id, pack_key):
    """
    Parse the pack manifest, and return
    a `StickerPack` object
    """
    manifest_resp = await http.get(CDN_MANIFEST_URL.format(
        pack_id=pack_id), timeout=None)
    if manifest_resp.status_code == 403:  # yes, 403, not 404
        raise NotFound(manifest_resp, "Sticker pack not found")
    if manifest_resp.status_code not in range(200, 300):
        raise HTTPException(manifest_resp, "Unhandled HTTP exception while downloading a sticker pack")

    manifest_encrypted = manifest_resp.content
    manifest_proto = decrypt(manifest_encrypted, pack_key)

    pb_pack = Pack()
    pb_pack.ParseFromString(manifest_proto)

    pack = StickerPack(pack_id, pack_key)
    pack.title = pb_pack.title
    pack.author = pb_pack.author

    cover = Sticker()
    cover.id = pb_pack.cover.id
    cover.emoji = pb_pack.cover.emoji
    pack.cover = cover

    for pb_sticker in pb_pack.stickers:
        sticker = Sticker()
        sticker.id = pb_sticker.id
        sticker.emoji = pb_sticker.emoji
        pack._addsticker(sticker)

    return pack


async def get_sticker(http, sticker_id, pack_id, pack_key):
    """
    Return the content of the webp file for a given sticker
    """
    sticker_resp = await http.get(
        CDN_STICKER_URL.format(pack_id=pack_id, sticker_id=sticker_id),
        timeout=None,
    )
    if sticker_resp.status_code == 403:  # same here, 403 is used instead of 404
        raise NotFound(sticker_resp, "Sticker not found")
    if sticker_resp.status_code not in range(200, 300):
        raise HTTPException(sticker_resp, "Unhandled HTTP exception while downloading a sticker")

    sticker_encrypted = sticker_resp.content
    sticker = decrypt(sticker_encrypted, pack_key)
    return sticker
