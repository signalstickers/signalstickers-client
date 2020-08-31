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

# Set here the pack title and author
pack.title = 'Hello world!'
pack.author = "Romain Ricard"

# Add the stickers here, with their emoji
# Accepted format:
# - Non-animated webp
# - PNG
# - GIF <100kb for animated stickers

add_sticker("/tmp/1.webp", "🤪")
add_sticker("/tmp/2.gif", "🐻")


# Specifying a cover is optionnal
# By default, the first sticker is the cover
cover = Sticker()
cover.id = pack.nb_stickers
# Set the cover file here
with open("/tmp/3.webp", "rb") as f_in:
    cover.image_data = f_in.read()
pack.cover = cover


# Instanciate the client with your Signal crendentials
client = StickersClient("YOUR_SIGNAL_USER", "YOUR_SIGNAL_PASS")

# Upload the pack
pack_id, pack_key = client.upload_pack(pack)

print("Pack uploaded!\n\nhttps://signal.art/addstickers/#pack_id={}&pack_key={}".format(pack_id, pack_key))