import io
import struct

import numpy as np
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from PIL import Image


class CyberShieldStego:
    def _derive_key(self, password, salt):
        return PBKDF2(password, salt, dkLen=32, count=100000)

    def encrypt(self, message, password):
        salt = get_random_bytes(16)
        iv = get_random_bytes(16)
        key = self._derive_key(password, salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
        return salt + iv + ciphertext

    def decrypt(self, data, password):
        try:
            salt = data[:16]
            iv = data[16:32]
            ct = data[32:]
            key = self._derive_key(password, salt)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = unpad(cipher.decrypt(ct), AES.block_size)
            return plaintext.decode('utf-8')
        except Exception as exc:
            raise ValueError('Decryption failed') from exc

    def _bytes_to_bits(self, data):
        bits = []
        for byte in data:
            for i in range(8):
                bits.append((byte >> (7 - i)) & 1)
        return bits

    def _bits_to_bytes(self, bits):
        result = bytearray()
        for i in range(0, len(bits), 8):
            chunk = bits[i:i + 8]
            if len(chunk) < 8:
                break
            result.append(sum(b << (7 - j) for j, b in enumerate(chunk)))
        return bytes(result)

    def get_capacity(self, img):
        width, height = img.size
        return max(0, (width * height * 3) // 8 - 52)

    def hide(self, image_bytes, message, password):
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        arr = np.array(img, dtype=np.uint8)

        payload = self.encrypt(message, password)
        header = struct.pack('>I', len(payload))
        bits = self._bytes_to_bits(header + payload)

        if len(bits) > arr.size:
            raise ValueError('Message too large for this image')

        flat = arr.flatten()
        for i, bit in enumerate(bits):
            flat[i] = (flat[i] & 0xFE) | bit
        arr = flat.reshape(arr.shape)

        out = io.BytesIO()
        Image.fromarray(arr).save(out, format='PNG', optimize=False)
        return out.getvalue()

    def extract(self, image_bytes, password):
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        arr = np.array(img, dtype=np.uint8).flatten()

        header_bits = [int(arr[i] & 1) for i in range(32)]
        header_bytes = self._bits_to_bytes(header_bits)
        data_length = struct.unpack('>I', header_bytes)[0]

        if data_length == 0 or 32 + data_length * 8 > len(arr):
            raise ValueError('No hidden data found')

        data_bits = [int(arr[i] & 1) for i in range(32, 32 + data_length * 8)]
        payload = self._bits_to_bytes(data_bits)

        return self.decrypt(payload, password)
