import anyio
import httpx
from signalstickers_client.models.sticker import Sticker
from signalstickers_client.models.sticker_pack import StickerPack
from signalstickers_client.urls import CDN_MANIFEST_URL, CDN_STICKER_URL
from signalstickers_client.classes.signalcrypto import decrypt
from signalstickers_client.utils.ca import CACERT_PATH
from signalstickers_client.classes.Stickers_pb2 import Pack


"""
This module allows to get full sticker packs, contains both data and metadata
"""


async def get_pack(pack_id, pack_key):
    """
    Return a `StickerPack` from its id and key
    """
    async with httpx.AsyncClient(verify=CACERT_PATH) as http:
        pack = await _get_pack(http, pack_id, pack_key)

        async def get_sticker_image(sticker):
            sticker.image_data = await _get_sticker(http, sticker.id, pack_id, pack_key)

        async with anyio.create_task_group() as tg:
            # The StickerPack object is created, but stickers and cover
            # are still missing the raw_image
            await tg.spawn(get_sticker_image, pack.cover)
            for sticker in pack.stickers:
                await tg.spawn(get_sticker_image, sticker)

    return pack


async def _get_pack(http, pack_id, pack_key):
    """
    Parse the pack manifest, and return
    a `StickerPack` object
    """
    manifest_req = await http.get(CDN_MANIFEST_URL.format(
        pack_id=pack_id))
    manifest_encrypted = bytes(manifest_req.content)
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


async def _get_sticker(http, sticker_id, pack_id, pack_key):
    """
    Return the content of the webp file for a given sticker
    """
    sticker_req = await http.get(
        CDN_STICKER_URL.format(pack_id=pack_id, sticker_id=sticker_id),
    )
    sticker_encrypted = bytes(sticker_req.content)
    sticker = decrypt(sticker_encrypted, pack_key)
    return sticker
