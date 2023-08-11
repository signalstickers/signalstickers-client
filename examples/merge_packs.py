import anyio
import os
from urllib.parse import parse_qs, urlparse

from signalstickers_client import StickersClient
from signalstickers_client.models import LocalStickerPack, Sticker


async def main():
    # List of signal.art packs urls
    packs = [
        "https://signal.art/addstickers/#pack_id=FIXME&pack_key=FIXME",
        "https://signal.art/addstickers/#pack_id=FIXME&pack_key=FIXME",
        "https://signal.art/addstickers/#pack_id=FIXME&pack_key=FIXME",
        "https://signal.art/addstickers/#pack_id=FIXME&pack_key=FIXME",
        "https://signal.art/addstickers/#pack_id=FIXME&pack_key=FIXME",
    ]

    new_pack = LocalStickerPack()
    new_pack.title = "My new combo pack!"
    new_pack.author = "Romain Ricard"

    id_offset = 0

    for pack_url in packs:
        pack_info = parse_qs(urlparse(pack_url).fragment)
        async with StickersClient() as client:
            old_pack = await client.get_pack(
                pack_info["pack_id"][0], pack_info["pack_key"][0]
            )

        nb_stickers = 0
        for sticker in old_pack.stickers:
            if sticker.image_data:  # Sometimes, stickers are HTTP 403 for... reasons
                nb_stickers += 1
                new_stick = Sticker()
                new_stick.id = sticker.id + id_offset
                new_stick.emoji = sticker.emoji
                new_stick.image_data = sticker.image_data
                new_pack._addsticker(new_stick)

        id_offset += nb_stickers

    async with StickersClient(
        os.environ["SIGNAL_USER"], os.environ["SIGNAL_PASS"]
    ) as client:
        # Upload the pack
        pack_id, pack_key = await client.upload_pack(new_pack)

    print(
        "Pack uploaded!\nhttps://signal.art/addstickers/#pack_id={}&pack_key={}".format(
            pack_id, pack_key
        )
    )
    print(
        "\nPreview\nhttps://signalstickers.com/pack/{}?key={}".format(pack_id, pack_key)
    )


if __name__ == "__main__":
    anyio.run(main)
