from typing import Iterator, Protocol

from signalstickers_client.models.sticker import Sticker

class StickersList(Protocol):
    def add(self) -> Sticker: ...
    def __iter__(self) -> Iterator[Sticker]: ...
    def __next__(self) -> Sticker: ...

class Pack:
    title: str
    author: str
    cover: Sticker
    stickers: StickersList

    def ParseFromString(self, data: bytes) -> None: ...
    def SerializeToString(self) -> bytes: ...
