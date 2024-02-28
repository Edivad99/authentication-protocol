from socket import socket
import struct
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
    self.send_msg(M1.encode())

  def receiveM1(self):
    recv = self.recv_msg()
    M1 = recv.decode()
    id_client = M1.split("#")[0]
    session_id = M1.split("#")[1]
    return id_client, session_id

  def sendM2(self, C1: list[int], r1: int):
    M2 = f"{C1}#{r1}"
    self.send_msg(M2.encode())

  def receiveM2(self):
    recv = self.recv_msg()
    M2 = recv.decode()
    C1_raw = M2.split("#")[0]
    C1 = covert_str_list_to_int_list(C1_raw)
    r1 = int(M2.split("#")[1])
    return C1, r1

  def sendM3(self, k1: bytes, r1: int, t1: bytes, C2: list[int], r2: int):
    payload = f"{r1}#{list(t1)}#{C2}#{r2}"
    M3 = encrypt(k1, payload.encode())
    self.send_msg(M3)

  def receiveM3(self):
    M3 = self.recv_msg()
    return M3

  def sendM4(self, M4: bytes):
    print(f"len(M4): {len(M4)}")
    self.send_msg(M4)

  def receiveM4(self):
    M4 = self.recv_msg()
    print(f"len(M4): {len(M4)}")
    return M4

  def sendMessageEncrypted(self, T: bytes, message: bytes):
    encrypted = encrypt(T, message)
    self.send_msg(encrypted)

  def receiveMessageEncrypted(self, T: bytes):
    encrypted = self.recv_msg()
    return decrypt(T, encrypted)
  
  def send_msg(self, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    self.socket.sendall(msg)

  def recv_msg(self):
    # Read message length and unpack it into an integer
    raw_msglen = self.recvall(4)
    if not raw_msglen:
      return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return self.recvall(msglen)

  def recvall(self, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
      packet = self.socket.recv(n - len(data))
      if not packet:
        return None
      data.extend(packet)
    return bytes(data)