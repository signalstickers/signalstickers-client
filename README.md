# Python client for Signal stickers

A client to interact with the [Signal](https://signal.org/) stickers API.

+ Fetch sticker packs
+ Get images files
+ etc.


> Note: despite its name, this client does not interacts with
> `signalstickers.com`, so information defined there (tags, etc.) will **not**
> be fetched.

> This client connects to the Signal sticker API. Please **do not flood it**.

## Installation

```bash
pip install --user signalstickers-client
```

This module requires `cryptography` (but it should be installed with the
previous command).
 
## Usage

The `StickerPack` object returned by `StickersClient().get_pack(<pack_id>,
<pack_key>)` exposes the following attributes:

+ `id` (string): the pack id. Equals to `pack_id`;
+ `key` (string): the pack key. Equals to `pack_key`;
+ `title` (string): the title of the pack;
+ `author` (string): the author of the pack;
+ `nb_stickers` (int): the number of stickers in the pack;
+ `cover` (`Sticker`): the cover sticker;
+ `stickers` (list): the list of stickers in the pack (which are `Sticker`
  objects).


A `Sticker` object exposes the following attributes:

+ `id` (int): the id of the sticker in the pack;
+ `emoji` (string): the emoji mapped to this sticker;
+ `image_data` (bytes): the webp image of the sticker.


## Example usage

```python
import os
from signalstickers_client import StickersClient


# "Friends of the Internet" by Bits of Freedom
pack_id = "4830e258138fca961ab2151d9596755c"
pack_key = "87078ee421bad8bf44092ca72166b67ae5397e943452e4300ced9367b7f6a1a1"


client = StickersClient()
pack = client.get_pack(pack_id, pack_key)

print(pack.title)  # "Friends of the Internet"
print(pack.author)  # "Bits of Freedom"
print(pack.nb_stickers)  # 7

# Saves all stickers in webp format in /tmp/stickersclient
# if the directory exists
for sticker in pack.stickers:
    with open(
        os.path.join("/tmp", "stickersclient", "{}.webp".format(sticker.id)), "wb"
    ) as sticker_f:
        sticker_f.write(sticker.image_data)

```


## License

See [LICENSE](https://github.com/romainricard/signalstickers-client/blob/master/LICENSE)


## Legal

This is not an official Signal project. This is an independant project.  
Signal is a registered trademark in the United States and other countries.


## Author

Romain Ricard <contact+stickerclient@romainricard.fr>
