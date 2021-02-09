#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signalstickers_client.classes.Stickers_pb2 as protobuf_stickers


class LocalStickerPack:
    """
    Represent a Local Sticker Pack, i.e. a pack that has not been uploaded yet
    to Signal servers.
    """

    def __init__(self):
        self.title = None
        self.author = None
        self.stickers = []
        self.cover = None

    @property
    def nb_stickers(self):
        """
        Return the number of stickers in the pack
        """
        return len(self.stickers)

    @property
    def nb_stickers_with_cover(self):
        """
        Return the number of stickers in the pack, including the cover
        """
        return len(self.stickers) + 1 if self.cover else len(self.stickers)

    @property
    def manifest(self):
        manifest = protobuf_stickers.Pack()
        manifest.title = self.title
        manifest.author = self.author

        cover = manifest.cover

        if self.cover:
            cover.id = self.cover.id
            cover.emoji = ""
        else:
            # Take the first sticker as the cover
            cover.id = 0

        for sticker in self.stickers:
            sticker_manifest = manifest.stickers.add()
            sticker_manifest.id = sticker.id
            sticker_manifest.emoji = sticker.emoji

        return manifest.SerializeToString()

    def _addsticker(self, sticker):
        """
        Add the binary content (which is a webp image) to
        the `StickerPack`' list of stickers
        """
        self.stickers.append(sticker)
