import requests
from signalstickers_client.models.sticker import Sticker
from signalstickers_client.models.sticker_pack import StickerPack
from signalstickers_client.urls import CDN_MANIFEST_URL, CDN_STICKER_URL
from signalstickers_client.classes.signalcrypto import decrypt
from signalstickers_client.utils.ca import CACERT_PATH
from signalstickers_client.classes.Stickers_pb2 import Pack


"""
This module allows to get full sticker packs, contains both data and metadata
"""


def get_pack(pack_id, pack_key):
    """
    Return a `StickerPack` from its id and key
    """
    pack = _get_pack(pack_id, pack_key)

    # The StickerPack object is created, but stickers and cover
    # are still missing the raw_image
    pack.cover.image_data = _get_sticker(pack.cover.id, pack_id, pack_key)
    for sticker in pack.stickers:
        sticker.image_data = _get_sticker(sticker.id, pack_id, pack_key)

    return pack


def _get_pack(pack_id, pack_key):
    """
    Parse the pack manifest, and return
    a `StickerPack` object
    """
    manifest_req = requests.get(CDN_MANIFEST_URL.format(
        pack_id=pack_id), verify=CACERT_PATH)
    manifest_encrypted = manifest_req.content
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


def _get_sticker(sticker_id, pack_id, pack_key):
    """
    Return the content of the webp file for a given sticker
    """
    sticker_req = requests.get(
        CDN_STICKER_URL.format(pack_id=pack_id, sticker_id=sticker_id),
        verify=CACERT_PATH
    )
    sticker_encrypted = sticker_req.content
    sticker = decrypt(sticker_encrypted, pack_key)
    return sticker
