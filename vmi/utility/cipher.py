from Crypto.Cipher import Blowfish
import base64
import sys
from binascii import hexlify, unhexlify

class InvalidBlockSizeError(Exception):
        """Raised for invalid block sizes"""
        pass

class PKCS7Encoder():
    """
    Technique for padding a string as defined in RFC 2315, section 10.3,
    note #2
    """
    def __init__(self, block_size=16):
        if block_size < 1 or block_size > 99:
            raise InvalidBlockSizeError('The block size must be between 1 ' \
                    'and 99')
        self.block_size = block_size

    def encode(self, text):
        text_length = len(text)
        amount_to_pad = self.block_size - (text_length % self.block_size)
        if amount_to_pad == 0:
            amount_to_pad = self.block_size
        pad = unhexlify('%02d' % amount_to_pad)
        return text + pad * amount_to_pad

    def decode(self, text):
        pad = int("0x"+hexlify(text[-1]), 16)
        return text[:-pad]


class BFCipher:
    def __init__(self, pword):
        self.__cipher = Blowfish.new(pword)
        self.__padder = PKCS7Encoder(8)
    def encrypt(self, text):
        ciphertext = self.__cipher.encrypt(self.__pad_file(text))
        return base64.b64encode(ciphertext)
    def decrypt(self, msg):
        data = base64.b64decode(msg)
        cleartext = self.__depad_file(self.__cipher.decrypt(data))
        return cleartext
    # Blowfish cipher needs 8 byte blocks to work with
    def __pad_file(self, file_buffer):
        return self.__padder.encode(file_buffer)
    
    def __depad_file(self, file_buffer):
        return self.__padder.decode(file_buffer)
    
def decode_with_hex_bf_pkcs7(key, text):
    bf = Blowfish.new(key)
    pkcs7 = PKCS7Encoder(8)
    return pkcs7.decode(bf.decrypt(unhexlify(text)))    

def encode_with_pkcs7_bf(key, text):
    bf = Blowfish.new(key)
    pkcs7 = PKCS7Encoder(8)
    return hexlify(bf.encrypt(pkcs7.encode(text))).upper() 
