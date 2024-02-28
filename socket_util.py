from socket import socket
from util import (
    covert_str_list_to_int_list,
    encrypt,
    decrypt
  )

class SocketUtil:

  def __init__(self, socket: socket):
    self.socket = socket

  def sendM1(self, id: int, session_id: int):
    M1 = f"{id}#{session_id}"
    self.socket.sendall(M1.encode())

  def receiveM1(self):
    recv = self.socket.recv(1024)
    M1 = recv.decode()
    id_client = M1.split("#")[0]
    session_id = M1.split("#")[1]
    return id_client, session_id

  def sendM2(self, C1: list[int], r1: int):
    M2 = f"{C1}#{r1}"
    self.socket.sendall(M2.encode())

  def receiveM2(self):
    recv = self.socket.recv(1024)
    M2 = recv.decode()
    C1_raw = M2.split("#")[0]
    C1 = covert_str_list_to_int_list(C1_raw)
    r1 = int(M2.split("#")[1])
    return C1, r1

  def sendM3(self, k1: bytes, r1: int, t1: bytes, C2: list[int], r2: int):
    payload = f"{r1}#{list(t1)}#{C2}#{r2}"
    M3 = encrypt(k1, payload.encode())
    self.socket.sendall(M3)

  def receiveM3(self):
    M3 = self.socket.recv(1024)
    return M3

  def sendM4(self, M4: bytes):
    self.socket.sendall(M4)

  def receiveM4(self):
    M4 = self.socket.recv(1024)
    return M4

  def sendMessageEncrypted(self, T: bytes, message: bytes):
    encrypted = encrypt(T, message)
    self.socket.sendall(encrypted)

  def receiveMessageEncrypted(self, T: bytes):
    encrypted = self.socket.recv(1024)
    return decrypt(T, encrypted)