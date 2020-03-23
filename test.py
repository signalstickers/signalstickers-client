import os
from stickersclient import StickersClient


# "Friends of the Internet" by Bits of Freedom
pack_id = "4830e258138fca961ab2151d9596755c"
pack_key = "87078ee421bad8bf44092ca72166b67ae5397e943452e4300ced9367b7f6a1a1"

# pack_id = "8e21a5bde99182638d40c7d70c8c954d"
# pack_key = "fd4f26e2952fac93e8304713db4c493eb0b2247fe08b2385342db80e3471c8d5"


client = StickersClient()
pack = client.get_pack(pack_id, pack_key)

print(pack.title)  # "Friends of the Internet"
print(pack.author)  # "Bits of Freedom"
print(pack.nb_stickers)  # 7

# Saves all stickers in webp format in /tmp/stickersclient
for sticker in pack.stickers:
    with open(
        os.path.join("/tmp", "stickersclient", "{}.webp".format(sticker.id)), "wb"
    ) as sticker_f:
        sticker_f.write(sticker.image_data)
