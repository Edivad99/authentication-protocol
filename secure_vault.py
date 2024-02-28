import os
import pickle

N = 10 # n keys
M = 32 # m bits each keys

def load_secure_vault(type: str) -> list[bytes]:
  with open(f"secure_vault_{type}.sv", 'rb') as f:
    return pickle.load(f)

def regen_secure_vault():
  secure_vault = []
  for _ in range(N):
    secure_vault.append(os.urandom(M))

  with open(f"secure_vault_client.sv", "wb") as f:
    pickle.dump(secure_vault, f, pickle.HIGHEST_PROTOCOL)
  with open(f"secure_vault_server.sv", "wb") as f:
    pickle.dump(secure_vault, f, pickle.HIGHEST_PROTOCOL)
