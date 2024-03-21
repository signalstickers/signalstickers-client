#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List, Optional

from signalstickers_client.models.sticker import Sticker


class StickerPack:
    """
    Represent a Sticker Pack
    """

    def __init__(self, id: str, key: str):
        self.id: str = id
        self.key: str = key
        self.title: Optional[str] = None
        self.author: Optional[str] = None
        self.cover: Optional[Sticker] = None
        self.stickers: List[Sticker] = []

    @property
    def nb_stickers(self):
        """
        Return the number of stickers in the pack
        """
        return len(self.stickers)

    def _addsticker(self, sticker: Sticker):
        """
        Add the binary content (which is a webp image) to
        the `StickerPack`' list of stickers
        """
        self.stickers.append(sticker)
