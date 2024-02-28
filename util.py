import random
import base64
import os
from secure_vault import SecureVault
from cryptography.fernet import Fernet

def covert_str_list_to_int_list(x1: str) -> list[int]:
  return [int(x) for x in x1.strip("][").split(", ")]

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

def generate_session_key() -> bytes:
  return os.urandom(SecureVault.M)

def unpack_M3(payload: str) -> tuple[int, bytes, list[int], int]:
  r1 = int(payload.split("#")[0])
  t1 = bytes(covert_str_list_to_int_list(payload.split("#")[1]))
  C2 = covert_str_list_to_int_list(payload.split("#")[2])
  r2 = int(payload.split("#")[3])
  return r1, t1, C2, r2

def unpack_M4(payload: str) -> tuple[int, bytes]:
  r2 = int(payload.split("#")[0])
  t2 = bytes(covert_str_list_to_int_list(payload.split("#")[1]))
  return r2, t2