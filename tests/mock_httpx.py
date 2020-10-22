from os.path import join, dirname


def get_data_from_url(url):
    """
    Depending on the URL, returns the bin data of the requested file
    """
    splitted_url = url.split("/")

    if splitted_url[-2] == "full":
        # Getting indivitual stickers
        pack_id = splitted_url[-3]
        filename = f"{splitted_url[-1]}.bin"
    else:
        # Getting manifest
        pack_id = splitted_url[-2]
        filename = "manifest.bin"

    file_path = join(dirname(__file__), "test_data", pack_id, filename)

    with open(file_path, "rb") as f_in:
        data = f_in.read()
    return data


class MockResponse:
    """
    Used to monkeypatch `httpx`'s response
    """

    def __init__(self, url):
        self.content_data = get_data_from_url(url)

    @staticmethod
    def raise_for_status():
        pass

    @property
    def content(self):
        return self.content_data


class MockHttpx:
    """
    Used to monkeypatch `httpx`
    """

    @staticmethod
    def __init__(*args, **kwargs):
        pass

    @staticmethod
    async def __aenter__(*args, **kwargs):
        return MockHttpx

    @staticmethod
    async def __aexit__(*args, **kwargs):
        pass

    @staticmethod
    async def get(*args, **kwargs):
        return MockResponse(url=args[0])
