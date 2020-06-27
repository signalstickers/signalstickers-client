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

from signalstickers_client.classes import downloader, uploader
from signalstickers_client.models import Sticker, StickerPack, LocalStickerPack


class StickersClient:

  def __init__(self, signal_user="", signal_pass=""):
      self.signal_user = signal_user
      self.signal_pass = signal_pass

  def get_pack(self, pack_id, pack_key):
      """
      Return a `StickerPack` from its id and key
      """
      return downloader.get_pack(pack_id, pack_key)

  def upload_pack(self, pack: LocalStickerPack):
      """
      Upload a `LocalStickerPack` and return its `pack_id` and `pack_key`
      """
      return uploader.upload_pack(pack, self.signal_user, self.signal_pass)
