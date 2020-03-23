#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from binascii import unhexlify
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from urllib import request


class StickerPack:
    """
    Represents a Sticker Pack
    """

    def __init__(self, id, key):
        self.id = id
        self.key = key
        self.title = None
        self.author = None
        self.cover = None
        self.stickers = []

    @property
    def nb_stickers(self):
        """
        Returns the number of stickers in the pack
        """
        return len(self.stickers)

    def _addsticker(self, sticker):
        """
        Adds the binary content (which is a webp image) to
        the `StickerPack`' list of stickers
        """
        self.stickers.append(sticker)


class Sticker:
    """
    Represents a Sticker
    """

    def __init__(self):
        self.id = None
        self.emoji = None
        self.image_data = None


class StickersClient:
    """
    This class gives tools to interact with the Signal stickers API,
    and allows to get full sticker packs, contains both data and metadata
    """

    def __init__(self):
        self.api_baseurl = "https://cdn-ca.signal.org/stickers/{pack_id}/"
        self.api_manifesturl = self.api_baseurl + "manifest.proto"
        self.api_stickerurl = self.api_baseurl + "full/{sticker_id}"

    def get_pack(self, pack_id, pack_key):
        """
        Return a `StickerPack` from its id and key
        """
        pack = self._get_pack(pack_id, pack_key)

        # The StickerPack object is created, but stickers and cover
        # are still missing the raw_image
        pack.cover.image_data = self._get_sticker(pack.cover.id, pack_id, pack_key)
        for sticker in pack.stickers:
            sticker.image_data = self._get_sticker(sticker.id, pack_id, pack_key)

        return pack

    def _get_pack(self, pack_id, pack_key):
        """
        Parses the pack manifest, and return
        a `StickerPack` object
        """
        manifest_req = request.urlopen(self.api_manifesturl.format(pack_id=pack_id))
        manifest_encrypted = manifest_req.read()
        manifest_proto = self._decrypt(manifest_encrypted, pack_id, pack_key)

        # For a reason that I can't explain, it was impossible to use Google's
        # python protocolbuffers lib to handle the manifest, so I created my own.
        # See https://developers.google.com/protocol-buffers/docs/encoding
        # and https://github.com/protobufjs/protobuf.js/wiki/How-to-reverse-engineer-a-buffer-by-hand
        # for references

        protobuf = PackProtobuf(pack_id, pack_key)
        protobuf.parse_protobuf(manifest_proto)

        return protobuf.pack

    def _get_sticker(self, sticker_id, pack_id, pack_key):
        """
        Returns the content of the webp file for a given sticker
        """
        sticker_req = request.urlopen(
            self.api_stickerurl.format(pack_id=pack_id, sticker_id=sticker_id)
        )
        sticker_encrypted = sticker_req.read()
        sticker = self._decrypt(sticker_encrypted, pack_id, pack_key)
        return sticker

    def _decrypt(self, encrypted_data, pack_id, pack_key):
        """
        Decrypts a manifest or an image
        """
        aes_key, hmac_key = self._derive_key(pack_id, pack_key)

        pack_iv = encrypted_data[0:16]
        pack_ciphertext_body = encrypted_data[16:-32]
        pack_hmac = encrypted_data[-32:]
        pack_combined = encrypted_data[0:-32]

        # Check that HMAC is correct
        hmac_o = hmac.HMAC(hmac_key, hashes.SHA256(), default_backend())
        hmac_o.update(pack_combined)
        hmac_o.verify(pack_hmac)

        cipher = Cipher(AES(aes_key), CBC(pack_iv), default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(pack_ciphertext_body) + decryptor.finalize()

    def _derive_key(self, pack_id, pack_key):
        """
        Derives the pack_key, and returns a `aes_key` and a `hmac_key`
        """
        backend = default_backend()
        info = b"Sticker Pack"
        length = 512
        hash_algorithm = hashes.SHA256()

        hkdf = HKDF(
            algorithm=hash_algorithm,
            length=length,
            salt=None,
            info=info,
            backend=backend,
        )

        # Kids, don't forget `unhexlify`, it took me 3hrs to figure it out
        key = hkdf.derive(unhexlify(pack_key))
        aes_key = key[0:32]
        hmac_key = key[32:64]

        return aes_key, hmac_key


class PackProtobuf:
    """
    This class is able to process a `manifest.proto` file from the Signal
    stickers API.

    It should be instanciated for each pack, and the processed, bare
    `StickerPack` is accessible via its property `pack`.

    Note: this parser is SPECIFIC to Signal's `Stickers.proto`
    (https://signal.art/addstickers/Stickers.proto). You can reuse it if you
    want to understand Protocol Buffers/need a protobuf parser, but you'll have
    to modify it according to your needs.
    """

    def __init__(self, pack_id, pack_key):
        self.pack = StickerPack(pack_id, pack_key)

        # These two properties will hold data for the currently processed pack
        self._current_sticker_id = None
        self._current_sticker_emoji = None

    def parse_protobuf(self, bin_data, embedded_item=False):
        """
        Parses raw protocolbuffer
        """

        buffer = bin_data

        while len(buffer):
            # Get the item metadata
            item_tag = buffer[0]
            item_wire_type = item_tag & 7
            item_field_id = item_tag >> 3

            # Yes, item_wire_type == data_offset, but I kept data_offset
            # for clarity

            if item_wire_type == 2:  #  string or embedded message
                item_size = buffer[1]
                data_offset = 2
            if item_wire_type == 0:  #  uint32
                item_size = 2
                data_offset = 0

            item_data = buffer[data_offset : item_size + data_offset]

            buffer = buffer[data_offset + item_size :]

            # Sometimes, the manifest is padded with garbage.
            #  Can't figure out why.
            # TODO solve this mystery. Any help appreciated!
            if len(item_data) != item_size:
                break

            self.parse_item(item_field_id, item_data, embedded_item)

    def parse_item(self, item_field_id, item_data, embedded_item=False):
        """
        Parses item and embedded items, and matches them with objects types
        we know (`StickerPack` and `Sticker`)
        """
        #  Title
        if item_field_id == 1 and not embedded_item:
            self.pack.title = item_data.decode("utf-8")

        # Author
        elif item_field_id == 2 and not embedded_item:
            self.pack.author = item_data.decode("utf-8")

        # Cover
        elif item_field_id == 3:
            # Parse the embedded item
            self.parse_protobuf(item_data, True)
            cover = Sticker()
            cover.id = self._current_sticker_id[1]
            cover.emoji = self._current_sticker_emoji
            self.pack.cover = cover

        # Sticker
        elif item_field_id == 4:
            # Parse the embedded item
            self.parse_protobuf(item_data, True)
            sticker = Sticker()
            sticker.id = self._current_sticker_id[1]
            sticker.emoji = self._current_sticker_emoji
            self.pack._addsticker(sticker)

        # Sticker id
        elif item_field_id == 1 and embedded_item:
            self._current_sticker_id = item_data

        # Sticker emoji
        elif item_field_id == 2 and embedded_item:
            self._current_sticker_emoji = item_data.decode("utf-8")
