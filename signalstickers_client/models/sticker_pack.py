#!/usr/bin/env python
# -*- coding: utf-8 -*-

class StickerPack:
    """
    Represent a Sticker Pack
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
        Return the number of stickers in the pack
        """
        return len(self.stickers)

    def _addsticker(self, sticker):
        """
        Add the binary content (which is a webp image) to
        the `StickerPack`' list of stickers
        """
        self.stickers.append(sticker)
