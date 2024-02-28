import socket
import secure_vault
from socket_util import SocketUtil
from util import (
    list_xor,
    xor,
    encrypt,
    decrypt,
    generate_challenge,
    generate_session_key,
    unpack_M3
  )

def main():
  SERVER_HOST = '127.0.0.1'
  SERVER_PORT = 12345

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    server_socket.listen()

    print(f"Server in ascolto su {SERVER_HOST}:{SERVER_PORT}")
    while True:
      # Accetta la connessione
      conn, addr = server_socket.accept()
      with conn:
        socket_util = SocketUtil(conn)
        print(f"Connessione accettata da {addr}")
        ID_CLIENT, SESSION_ID = socket_util.receiveM1()
        #print(f"ID_CLIENT: {ID_CLIENT}")
        #print(f"SESSION_ID: {SESSION_ID}")

        # Check if ID_CLIENT is valid
        if (ID_CLIENT != "16"):
          return
        print("ID_CLIENT valido")

        # The challenge M2 contains a challenge C1 and a random number r1
        # C1 is a set of p distinct numbers, and each number represents an 
        # index of a key, stored in the secure vault. C1 is denoted as 
        # {c11, c12, c13…, c1p}. The value of p should be less than n.
        C1, r1 = generate_challenge(secure_vault.N)
        socket_util.sendM2(C1, r1)
        #------------------------------------------------
        M3 = socket_util.receiveM3()
        #print(f"M3: {M3}")
        K = secure_vault.load_secure_vault()
        k1 = list_xor([K[i] for i in C1])
        #print(f"k1: {k1}")
        payload = decrypt(k1, M3).decode()
        r1_client, t1, C2, r2 = unpack_M3(payload)

        # If the server retrieves r1 from the received message,
        # it generates a response to the challenge C2.
        if (r1_client != r1):
          print("Errore: r1 non corrisponde")
          return

        #print(f"C2: {C2}")
        k2 = list_xor([K[i] for i in C2])
        #print(f"k2: {k2}")
        xor_result = xor(k2, t1)
        #print(f"xor_result: {xor_result}")

        t2 = generate_session_key()
        payload_M4 = f"{r2}#{list(t2)}"
        #t2 = bytes(str(list(t2)), 'utf-8')
        #print(f"t2: {t2}")

        #print(f"payload: {payload_M4}")
        M4 = encrypt(xor_result, payload_M4.encode())
        #print(f"M4: {M4}")
        socket_util.sendM4(M4)
        #------------------------------------------------
        T = xor(t1, t2)
        socket_util.sendMessageEncrypted(T, b"Hello, world!")

if __name__ == "__main__":
    main()
