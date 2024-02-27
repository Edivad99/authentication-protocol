from socket import socket

from util import covert_str_list_to_int_list

class SocketUtil:

  def __init__(self, socket: socket):
    self.socket = socket

  @staticmethod
  def encode_int(x: int) -> bytes:
    return str(x).encode()

  def sendM1(self, id: int, session_id: int):
    M1 = f"{id}#{session_id}"
    print(f"M1: {M1}")
    self.socket.sendall(SocketUtil.encode_int(M1))

  def receiveM1(self):
    recv = self.socket.recv(1024)
    M1 = recv.decode()
    id_client = M1.split("#")[0]
    session_id = M1.split("#")[1]
    return id_client, session_id

  def sendM2(self, C1: list[int], r1: int):
    M2 = f"{C1}#{r1}"
    print(f"M2: {M2}")
    self.socket.sendall(M2.encode())

  def receiveM2(self):
    recv = self.socket.recv(1024)
    M2 = recv.decode()
    print(f"M2: {M2}")
    C1_raw = M2.split("#")[0]
    C1 = covert_str_list_to_int_list(C1_raw)
    r1 = M2.split("#")[1]
    return C1, r1

  def sendM3(self, M3: bytes):
    self.socket.sendall(M3)

  def receiveM3(self):
    M3 = self.socket.recv(1024)
    return M3

  def sendM4(self, M4: bytes):
    self.socket.sendall(M4)

  def receiveM4(self):
    M4 = self.socket.recv(1024)
    return M4