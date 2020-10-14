import pytest
import signalstickers_client

# This is the same as using the @pytest.mark.anyio on all test functions in the module
pytestmark = pytest.mark.anyio

@pytest.fixture
def client():
    return signalstickers_client.StickersClient()

async def test_downloadpack(client):
    # "Friends of the Internet" by Bits of Freedom
    # This pack works with Google's protobuf lib
    pack_id = "4830e258138fca961ab2151d9596755c"
    pack_key = "87078ee421bad8bf44092ca72166b67ae5397e943452e4300ced9367b7f6a1a1"

    async with client:
        pack = await client.get_pack(pack_id, pack_key)

    assert pack.title == "Friends of the Internet"
    assert pack.author == "Bits of Freedom"
    assert pack.nb_stickers == 7

async def test_downloadpack_gpb(client):

    # This pack didn't worked with Google Protobuf lib before
    # Should work now
    pack_id = "29337132d9860f918519da3030d96c83"
    pack_key = "613b3816910c7eaf7c0768885c2fbe97fe990d089a85cd9ca3e523ba56a5d15b"

    async with client:
        pack = await client.get_pack(pack_id, pack_key)

    assert pack.title == "Factorio"
    assert pack.author == "ratti"
    assert pack.nb_stickers == 9
