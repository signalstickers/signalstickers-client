import pytest
import signalstickers_client
import anyio
import httpx
import hashlib
from mock_httpx import MockHttpx


# This is the same as using the @pytest.mark.anyio on all test functions in the module
pytestmark = pytest.mark.anyio


def test_download(monkeypatch):
    """
    With a mocked httpx lib, test the whole "download" part.
    """

    async def get_pack(pack_id, pack_key):
        async with signalstickers_client.StickersClient() as client:
            pack = await client.get_pack(pack_id, pack_key)
            return pack

    pack_id = "8f827147a008bf8b24f4188be657aead"
    pack_key = "fe71f36085caa48e26f82ba68d08f96499da9866cc4867fd6f0e0ba3af827461"

    expected_files = {
        0: {
            "hash": "c0cf2508a09e38e926b2a86fd3389fbaa296d85f769f6a3dc9fc2f7c3b33e67d",
            "emoji": "🐟",
        },
        1: {
            "hash": "460a7d9b4c159a82097b6246f54c85a86da439f390d88cac2ba9d4c14f7e5754",
            "emoji": "💻",
        },
        "cover": {
            "hash": "c0cf2508a09e38e926b2a86fd3389fbaa296d85f769f6a3dc9fc2f7c3b33e67d",
            "emoji": "",
            "id": 0,
        },
    }

    monkeypatch.setattr(httpx, "AsyncClient", MockHttpx)

    pack = anyio.run(get_pack, pack_id, pack_key)

    # Check properties
    assert pack.id == pack_id
    assert pack.key == pack_key
    assert pack.title == "Test pack"
    assert pack.author == "Romain Ricard"
    assert pack.nb_stickers == 2
    assert len(pack.stickers) == 2

    # Check stickers
    for sticker in pack.stickers:
        assert (
            expected_files[sticker.id]["hash"]
            == hashlib.sha256(sticker.image_data).hexdigest()
        )
        assert expected_files[sticker.id]["emoji"] == sticker.emoji

    # Check cover
    assert (
        expected_files["cover"]["hash"]
        == hashlib.sha256(pack.cover.image_data).hexdigest()
    )
    assert expected_files["cover"]["emoji"] == pack.cover.emoji
    assert expected_files["cover"]["id"] == pack.cover.id
