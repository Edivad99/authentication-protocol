import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def covert_str_list_to_int_list(x1: list[str]) -> list[int]:
  x1 = x1.split(", ")
  x1[0] = x1[0].replace("[", "")
  x1[-1] = x1[-1].replace("]", "")
  x1 = [int(x) for x in x1]
  return x1

def xor(a: list[int], b: list[int]) -> list[int]:
  return [i ^ j for i, j in zip(a, b)]


def encrypt(key: bytes, plaintext: bytes) -> bytes:
  iv = os.urandom(16)
  cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
  encryptor = cipher.encryptor()
  ct = encryptor.update(plaintext) + encryptor.finalize()
  return ct

def decrypt(key: bytes, ciphertext: bytes) -> bytes:
  cipher = Cipher(algorithms.AES(key), modes.ECB())
  decryptor = cipher.decryptor()
  pt = decryptor.update(ciphertext) + decryptor.finalize()
  return pt


""" key = os.urandom(32)
iv = os.urandom(16)
cipher = Cipher(algorithms.AES(key))
encryptor = cipher.encryptor()
ct = encryptor.update(b"a secret message") + encryptor.finalize()
decryptor = cipher.decryptor()
decryptor.update(ct) + decryptor.finalize() """