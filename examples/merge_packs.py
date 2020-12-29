import anyio
import os
from signalstickers_client import StickersClient
from signalstickers_client.models import LocalStickerPack, Sticker


async def main():

    packs = [
        {
            "id": "pack1_id",
            "key": "pack1_key"
        },
        {
            "id": "pack2_id",
            "key": "pack2_key"
        },
        {
            "id": "pack3_id",
            "key": "pack3_key"
        }
    ]

    new_pack = LocalStickerPack()
    new_pack.title = 'My new combo pack!'
    new_pack.author = "Romain Ricard"

    for pack_data in packs:
        async with StickersClient() as client:
            old_pack = await client.get_pack(pack_data["id"], pack_data["key"])

        for sticker in old_pack.stickers:

            if sticker.image_data:  # Sometimes, stickers are HTTP 403 for... reasons
                new_stick = Sticker()
                new_stick.id = sticker.id
                new_stick.emoji = sticker.emoji
                new_stick.image_data = sticker.image_data
                new_pack._addsticker(new_stick)

    async with StickersClient(os.environ['SIGNAL_USER'], os.environ['SIGNAL_PASS']) as client:
        # Upload the pack
        pack_id, pack_key = await client.upload_pack(new_pack)

    print("Pack uploaded!\n\nhttps://signal.art/addstickers/#pack_id={}&pack_key={}".format(pack_id, pack_key))
    print("Preview\n\nhttps://signalstickers.com/pack/{}?key={}".format(pack_id, pack_key))

if __name__ == '__main__':
    anyio.run(main)
