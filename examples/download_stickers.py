import os
import anyio
from signalstickers_client import StickersClient

async def main():
    # "Friends of the Internet" by Bits of Freedom
    pack_id = "4830e258138fca961ab2151d9596755c"
    pack_key = "87078ee421bad8bf44092ca72166b67ae5397e943452e4300ced9367b7f6a1a1"


    async with StickersClient() as client:
        pack = await client.get_pack(pack_id, pack_key)

    print(pack.title)  # "Friends of the Internet"
    print(pack.author)  # "Bits of Freedom"
    print(pack.nb_stickers)  # 7

    async def save_sticker(sticker):
        async with await anyio.open_file(
            os.path.join("/tmp", "stickersclient", "{}.webp".format(sticker.id)),
            "wb",
        ) as f:
            await f.write(sticker.image_data)

    async with anyio.create_task_group() as tg:
        # Saves all stickers in webp format in /tmp/stickersclient in parallel
        # if the directory exists
        for sticker in pack.stickers:
            tg.start_soon(save_sticker, sticker)

if __name__ == '__main__':
    anyio.run(main)
