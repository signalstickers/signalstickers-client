import signalstickers_client
import unittest

class TestSignalStickersClient(unittest.TestCase):

    def test_downloadpack(self):
        # "Friends of the Internet" by Bits of Freedom
        # This pack works with Google's protobuf lib
        pack_id = "4830e258138fca961ab2151d9596755c"
        pack_key = "87078ee421bad8bf44092ca72166b67ae5397e943452e4300ced9367b7f6a1a1"

        pack = signalstickers_client.get_pack(pack_id, pack_key)

        self.assertEqual(pack.title, "Friends of the Internet")
        self.assertEqual(pack.author, "Bits of Freedom")
        self.assertEqual(pack.nb_stickers, 7)

    def test_downloadpack_gpb(self):

        # This pack didn't worked with Google Protobuf lib before
        # Should work now
        pack_id = "29337132d9860f918519da3030d96c83" 
        pack_key = "613b3816910c7eaf7c0768885c2fbe97fe990d089a85cd9ca3e523ba56a5d15b"

        pack = signalstickers_client.get_pack(pack_id, pack_key)

        self.assertEqual(pack.title, "Factorio")
        self.assertEqual(pack.author, "ratti")
        self.assertEqual(pack.nb_stickers, 9)


    def test_uploadpack(self):
        pass
        # can't really test to upload a sticker :(
        #self.assertEqual(signalstickers_client.upload_pack("foo"), "foo")


if __name__ == '__main__':
    unittest.main()
