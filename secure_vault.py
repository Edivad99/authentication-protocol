import os
import pickle
import hmac
import hashlib

class SecureVault:

  N = 4 # n keys
  M = int(256 / 8) # m bits each keys

  def __init__(self, type: str):
    self.type = type

  def load_secure_vault(self) -> list[bytes]:
    with open(f"secure_vault_{self.type}.sv", 'rb') as f:
      return pickle.load(f)

  def update_secure_vault(self, secure_vault: list[bytes], key: bytes):
    new_secure_vault = []
    for element in secure_vault:
      new_secure_vault.append(hmac.new(key, element, hashlib.sha256).digest())
    with open(f"secure_vault_{self.type}.sv", "wb") as f:
      pickle.dump(new_secure_vault, f, pickle.HIGHEST_PROTOCOL)

  @staticmethod
  def regen_secure_vault():
    secure_vault: list[bytes] = []
    for _ in range(SecureVault.N):
      secure_vault.append(os.urandom(SecureVault.M))

    with open(f"secure_vault_client.sv", "wb") as f:
      pickle.dump(secure_vault, f, pickle.HIGHEST_PROTOCOL)
    with open(f"secure_vault_server.sv", "wb") as f:
      pickle.dump(secure_vault, f, pickle.HIGHEST_PROTOCOL)
