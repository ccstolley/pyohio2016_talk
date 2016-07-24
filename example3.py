"""
An example of ctypes that handles bad inputs poorly.

Portions of this code were lifted (with light editing) from the
py-chef project at:
https://github.com/coderanger/pychef/blob/master/chef/rsa.py
"""
from ctypes import CDLL, c_int, c_void_p, c_ulong, create_string_buffer
from ctypes.util import find_library

libcrypto = CDLL(find_library('crypto'))

RSA_F4 = 0x10001
RSA_PKCS1_PADDING = 1

# int RSA_size(const RSA *rsa);
RSA_size = libcrypto.RSA_size
RSA_size.argtypes = [c_void_p]
RSA_size.restype = c_int

#int RSA_private_encrypt(int flen, unsigned char *from,
#    unsigned char *to, RSA *rsa,int padding);
RSA_private_encrypt = libcrypto.RSA_private_encrypt
RSA_private_encrypt.argtypes = [c_int, c_void_p, c_void_p, c_void_p, c_int]
RSA_private_encrypt.restype = c_int

#RSA *RSA_generate_key(int num, unsigned long e,
#    void (*callback)(int,int,void *), void *cb_arg);
RSA_generate_key = libcrypto.RSA_generate_key
RSA_generate_key.argtypes = [c_int, c_ulong, c_void_p, c_void_p]
RSA_generate_key.restype = c_void_p


class Key:
    """An OpenSSL RSA key."""

    def __init__(self):
        self.key = None
        self.public = False

    @classmethod
    def generate(cls, size=1024, exp=RSA_F4):
        self = cls()
        self.key = RSA_generate_key(size, exp, None, None)
        return self

    def private_encrypt(self, value, padding=RSA_PKCS1_PADDING):
        if not isinstance(value, bytes):
            buf = create_string_buffer(value.encode(), len(value))
        size = RSA_size(self.key)
        output = create_string_buffer(size)
        ret = RSA_private_encrypt(len(buf), buf, output, self.key, padding)
        if ret <= 0:
            raise ValueError('Unable to encrypt data')
        return output.raw[:ret]


###

k = Key.generate()
print(k.private_encrypt('foobar'))

k = Key()
print(k.private_encrypt('foobar'))
