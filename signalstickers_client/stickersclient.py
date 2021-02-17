#!/usr/bin/env python


"""
    Python client for the Signal stickers API.
    If you want to understand this code, you must be familiar with Signal
    stickers internals. tl;dr:
     - Everything in packs is encrypted on Signal's side;
     - Each pack has a manifest (`manifest.proto`), which gives the name of
       the pack, its author, and details (`id` and emoji) for the cover sticker
       and each of the stickers;
     - Manifest is serialized with Protocol Buffers;
     - Order of operations is:
        1. Get the manifest and decrypt it;
        2. Get details from the manifest, including stickers id;
        3. For each sticker and the cover, get the image (webp) thankd to their
           id, and decrypt them.

      This is what happens when you open a sticker pack in your Signal client,
      or what we reproduce on signalstickers.com .


    Please do not flood the Signal API (so don't put this code in a `while True` loop).

    Author: Romain RICARD <contact+stickerclient@romainricard.fr>
    License: LGPLv3
"""
import httpx

from signalstickers_client.classes import downloader, uploader
from signalstickers_client.models import LocalStickerPack
from signalstickers_client.utils.ca import CACERT_PATH


class StickersClient:
    def __init__(self, signal_user="", signal_pass=""):
        self.http: httpx.AsyncClient
        self.signal_user = signal_user
        self.signal_pass = signal_pass

    async def __aenter__(self) -> 'StickersClient':
        self.http = await httpx.AsyncClient(verify=CACERT_PATH).__aenter__()
        return self

    async def __aexit__(self, *excinfo):
        return await self.http.__aexit__(*excinfo)

    async def get_pack(self, pack_id, pack_key):
        """
        Return a `StickerPack` from its id and key
        """
        return await downloader.get_pack(self.http, pack_id, pack_key)

    async def get_pack_metadata(self, pack_id, pack_key):
        """
        Same as `.get_pack` but doesn't fetch the individual sticker images.
        """
        return await downloader.get_pack_metadata(self.http, pack_id, pack_key)

    async def download_sticker(self, sticker_id: int, pack_id, pack_key) -> bytes:
        """
        Return the image data for a given `sticker_id` belonging to the given `pack_id` and `pack_key`
        """
        return await downloader.get_sticker(self.http, sticker_id, pack_id, pack_key)

    async def upload_pack(self, pack: LocalStickerPack):
        """
        Upload a `LocalStickerPack` and return its `pack_id` and `pack_key`
        """
        return await uploader.upload_pack(self.http, pack, self.signal_user, self.signal_pass)
