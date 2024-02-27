import random
import base64
from cryptography.fernet import Fernet

def covert_str_list_to_int_list(x1: list[str]) -> list[int]:
  x1 = x1.split(", ")
  x1[0] = x1[0].replace("[", "")
  x1[-1] = x1[-1].replace("]", "")
  x1 = [int(x) for x in x1]
  return x1

def xor(a: bytes, b: bytes) -> bytes:
  return bytes([_a ^ _b for _a, _b in zip(a, b)])

def list_xor(a: list[bytes]) -> bytes:
  result = a[0]
  for i in range(1, len(a)):
    result = xor(result, a[i])
  return result

def encrypt(key: bytes, plaintext: bytes) -> bytes:
  key = base64.urlsafe_b64encode(key)
  f = Fernet(key)
  return f.encrypt(plaintext)

def decrypt(key: bytes, ciphertext: bytes) -> bytes:
  key = base64.urlsafe_b64encode(key)
  f = Fernet(key)
  return f.decrypt(ciphertext)

def generate_challenge(secure_vault_n : int) -> tuple[list[int], int]:
  p = random.randint(1, secure_vault_n - 1)
  C = random.sample(range(secure_vault_n), p)
  r = random.randint(1, 255)
  return C, r
