import random
import os
from secure_vault import SecureVault
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def covert_str_list_to_int_list(x1: str) -> list[int]:
  return [int(x) for x in x1.strip("][").split(", ")]

def xor(a: bytes, b: bytes) -> bytes:
  return bytes([_a ^ _b for _a, _b in zip(a, b)])

def list_xor(a: list[bytes]) -> bytes:
  result = a[0]
  for i in range(1, len(a)):
    result = xor(result, a[i])
  return result

def pad(s: bytes) -> bytes:
  BLOCK_SIZE = SecureVault.M
  return s + ((BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)).encode()

def unpad(s: bytes) -> bytes:
  return s[0 : -s[-1]]

def encrypt(key: bytes, plaintext: bytes) -> bytes:
  iv = b"0" * SecureVault.M
  cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
  encryptor = cipher.encryptor()
  ct = encryptor.update(pad(plaintext)) + encryptor.finalize()
  return ct

def decrypt(key: bytes, ciphertext: bytes) -> bytes:
  iv = b"0" * SecureVault.M
  cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
  decryptor = cipher.decryptor()
  decrypted = decryptor.update(ciphertext)
  return unpad(decrypted)

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