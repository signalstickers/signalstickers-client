# Python client for Signal stickers

A client to interact with Signal stickers API

+ Fetch sticker packs
+ Get images files
+ etc.

## Example usage

```python
import os
from stickersclient.stickersclient import StickersClient


# "Friends of the Internet" by Bits of Freedom
pack_id = "4830e258138fca961ab2151d9596755c"
pack_key = "87078ee421bad8bf44092ca72166b67ae5397e943452e4300ced9367b7f6a1a1"

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

```

## License

See [LICENSE.md](LICENSE.md)

## Author

Romain Ricard <contact+stickerclient@romainricard.fr>
