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
pip3 install --user signalstickers-client
```

This module requires `cryptography`, `protobuf`, `anyio`, and `httpx` (but they should
be installed with the previous command).
 
## Usage

If you are not familiar with Signal stickers, read
[STICKERS_INTERNALS.md](STICKERS_INTERNALS.md) first.

### Downloading a pack
The `StickerPack` object returned by `await StickersClient().get_pack(<pack_id>,
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


> **You will need your Signal credentials** To obtain them, run the Signal Desktop 
> app with the flag `--enable-dev-tools`, open the Developer Tools, and type
> `window.reduxStore.getState().items.uuid_id` to get your USER, and
> `window.reduxStore.getState().items.password` to get your PASSWORD.


## Example usage

[See `examples/`](examples/)

## Development

+ Create a `pipenv` with `pipenv install --dev`;
+ Edit the code you want;
+ Don't forget to launch tests with `pipenv run py.test`.

## License

See [LICENSE](https://github.com/romainricard/signalstickers-client/blob/master/LICENSE)


## Legal

This is not an official Signal project. This is an independant project.  
Signal is a registered trademark in the United States and other countries.


## Author

Romain Ricard <contact+stickerclient@romainricard.fr>
