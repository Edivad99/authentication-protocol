import socket
import random
from secure_vault import SecureVault

random.seed(1)

def main():
  SERVER_HOST = '127.0.0.1'
  SERVER_PORT = 12345

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    server_socket.listen()

    print(f"Server in ascolto su {SERVER_HOST}:{SERVER_PORT}")

    # Accetta la connessione
    conn, addr = server_socket.accept()
    with conn:
      print(f"Connessione accettata da {addr}")
      while True:
        data = conn.recv(1024)
        if not data:
          break
        M1 = data.decode()
        print(f"Dati ricevuti dal client: {M1}")
        ID_CLIENT = M1.split("#")[0]
        SESSION_ID = M1.split("#")[1]
        print(f"ID_CLIENT: {ID_CLIENT}")
        print(f"SESSION_ID: {SESSION_ID}")

        # Check if ID_CLIENT is valid
        if (ID_CLIENT != "16"):
          return

        # The challenge M2 contains a challenge C1 and a random number r1
        # C1 is a set of p distinct numbers, and each number represents an 
        # index of a key, stored in the secure vault. C1 is denoted as 
        # {c11, c12, c13…, c1p}. The value of p should be less than n.
        p = random.randint(1, SecureVault.N - 1)
        C1 = random.sample(range(SecureVault.N), p)
        r1 = random.randint(0, 255)
        M2 = f"{C1}#{r1}"
        print(f"M2: {M2}")

        print("ID_CLIENT valido")
        # Invia una risposta al client
        conn.sendall(M2.encode())
        #------------------------------------------------



if __name__ == "__main__":
    main()
