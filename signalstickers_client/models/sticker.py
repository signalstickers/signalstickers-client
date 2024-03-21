#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional


class Sticker:
    """
    Represent a Sticker
    """

    def __init__(self):
        self.id: Optional[int] = None
        self.emoji: Optional[str] = None
        self.image_data: Optional[bytes] = None
