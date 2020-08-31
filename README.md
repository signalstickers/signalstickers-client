# Python client for Signal stickers

A client to interact with the [Signal](https://signal.org/) stickers API.

+ Fetch sticker packs
+ Get images files
+ Upload sticker packs
+ etc.


> Note: despite its name, this client does not interacts with
> `signalstickers.com`, so information defined there (tags, etc.) will **not**
> be fetched.

> This client connects to the Signal sticker API. Please **do not flood it**.

## Installation

```bash
pip install --user signalstickers-client
```

This module requires `cryptography`, `protobuf` and `requests` (but they should
be installed with the previous command).
 
## Usage

### Downloading a pack
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


### Uploading a pack

Same thing, but use `LocalStickerPack` (that does not contains `id` and `key`)
instead of `StickerPack`.

## Example usage

_[See also `examples/`](examples/)_

### Downloading a pack

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

### Uploading a pack

```python
from signalstickers_client import StickersClient
from signalstickers_client.models import LocalStickerPack, Sticker


def add_sticker(path, emoji):

    stick = Sticker()
    stick.id = pack.nb_stickers
    stick.emoji = emoji

    with open(path, "rb") as f_in:
        stick.image_data = f_in.read()

    pack._addsticker(stick)


pack = LocalStickerPack()
pack.title = 'Hello world!'
pack.author = "Romain Ricard"

# webp or GIF, for animated stickers!
add_sticker("/tmp/1.webp", "🤪")
add_sticker("/tmp/2.gif", "🐻")

# Specifying a cover is optionnal
# By default, the first sticker is the cover
cover = Sticker()
cover.id = pack.nb_stickers
with open("/tmp/3.webp", "rb") as f_in:
    cover.image_data = f_in.read()
pack.cover = cover


# Instanciate the client with your Signal crendentials
client = StickersClient("YOUR_SIGNAL_USER", "YOUR_SIGNAL_PASS")

# Upload the pack
pack_id, pack_key = client.upload_pack(pack)

print("Pack uploaded!\n\nhttps://signal.art/addstickers/#pack_id={}&pack_key={}".format(pack_id, pack_key))
```

> **How to obtain your Signal credentials?**
> In Signal Desktop, open the Developer
> Tools, and type `window.reduxStore.getState().items.uuid_id` to get your USER,
> and `window.reduxStore.getState().items.password` to get your PASSWORD.



## License

See [LICENSE](https://github.com/romainricard/signalstickers-client/blob/master/LICENSE)


## Legal

This is not an official Signal project. This is an independant project.  
Signal is a registered trademark in the United States and other countries.


## Author

Romain Ricard <contact+stickerclient@romainricard.fr>
