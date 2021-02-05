from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac, padding
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


# Signal encrypted {sticker, manifest} are composed as follow:
#   iv (16) + encrypted data (n) + hmac (32)



def encrypt(plaintext, aes_key, hmac_key, iv):
    """
    Encrypt a manifest or an image
    """

    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update(plaintext)+ padder.finalize()

    cipher = Cipher(AES(aes_key), CBC(iv), default_backend())
    encryptor = cipher.encryptor()

    encrypted_data = encryptor.update(padded_plaintext) + encryptor.finalize()

    # Create the HMAC
    hmac_o = hmac.HMAC(hmac_key, hashes.SHA256(), default_backend())
    hmac_o.update(iv + encrypted_data)

    return iv + encrypted_data + hmac_o.finalize()


def decrypt(encrypted_data, pack_key):
    """
    Decrypt a manifest or an image
    """
    aes_key, hmac_key = derive_key(pack_key)

    pack_iv = encrypted_data[0:16]
    pack_ciphertext_body = encrypted_data[16:-32]
    pack_hmac = encrypted_data[-32:]
    pack_combined = encrypted_data[0:-32]

    # Check that HMAC is correct
    hmac_o = hmac.HMAC(hmac_key, hashes.SHA256(), default_backend())
    hmac_o.update(pack_combined)
    hmac_o.verify(pack_hmac)

    cipher = Cipher(AES(aes_key), CBC(pack_iv), default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(pack_ciphertext_body) + decryptor.finalize()

    # AES CBC uses padding, so let's unpad the data
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data)

    return unpadded_data + unpadder.finalize()


def derive_key(pack_key):
    """
    Derive a pack_key, and returns a `aes_key` and a `hmac_key`
    """
    info = b"Sticker Pack"
    length = 512
    hash_algorithm = hashes.SHA256()

    hkdf = HKDF(
        algorithm=hash_algorithm,
        length=length,
        salt=None,
        info=info,
        backend=default_backend(),
    )

    key = hkdf.derive(bytes.fromhex(pack_key))
    aes_key = key[0:32]
    hmac_key = key[32:64]

    return aes_key, hmac_key
