import os
import random
import sys

class SecureVault:

  N = 10 # n keys
  M = 16 # m bits each keys

  def __init__(self):
    random.seed(42)
    self.secure_vault = []

  def generate_secure_vault(self):
    # generate a key of length m bits
    key = os.urandom(self.M)
    # calculate the size of key
    key_size = len(key)
    print(f"key_size: {key_size}")
    print(f"key: {key}")

    for _ in range(self.N):
      self.secure_vault.append([random.randint(0, 255) for _ in range(self.M)])
    return self.secure_vault
