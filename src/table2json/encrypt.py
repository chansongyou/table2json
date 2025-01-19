from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64


class AESUtility:
    @staticmethod
    def encrypt(plain_text: str, key: str, iv: str):
        key_bytes = key.encode("utf-8")
        iv_bytes = iv.encode("utf-8")

        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        padded_data = pad(plain_text.encode("utf-8"), AES.block_size)
        encrypted_bytes = cipher.encrypt(padded_data)

        return base64.b64encode(encrypted_bytes).decode("utf-8")

    @staticmethod
    def decrypt(cipher_text: str, key: str, iv: str):
        key_bytes = key.encode("utf-8")
        iv_bytes = iv.encode("utf-8")

        encrypted_bytes = base64.b64decode(cipher_text)
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        decrypted_padded = cipher.decrypt(encrypted_bytes)
        decrypted_text = unpad(decrypted_padded, AES.block_size)

        return decrypted_text.decode("utf-8")
