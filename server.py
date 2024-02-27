import socket
import random
import secure_vault
from util import covert_str_list_to_int_list, list_xor, xor, encrypt, decrypt, generate_challenge

random.seed(1)

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
          print("ID_CLIENT valido")

          # The challenge M2 contains a challenge C1 and a random number r1
          # C1 is a set of p distinct numbers, and each number represents an 
          # index of a key, stored in the secure vault. C1 is denoted as 
          # {c11, c12, c13…, c1p}. The value of p should be less than n.
          C1, r1 = generate_challenge(secure_vault.N)
          M2 = f"{C1}#{r1}"
          print(f"M2: {M2}")

          # Invia una risposta al client
          conn.sendall(M2.encode())
          #------------------------------------------------
          M3 = conn.recv(1024)
          print(f"M3: {M3}")
          K = secure_vault.load_secure_vault()
          k1 = list_xor([K[i] for i in C1])
          print(f"k1: {k1}")
          payload = decrypt(k1, M3).decode()
          print(f"payload: {payload}")
          # If the server retrieves r1 from the received message,
          # it generates a response to the challenge C2.
          if (int(payload.split("#")[0]) != r1):
            print("Errore: r1 non corrisponde")
            return
          
          t1 = int(payload.split("#")[1])
          C2 = covert_str_list_to_int_list(payload.split("#")[2])
          r2 = int(payload.split("#")[3])
          print(f"t1: {t1}")
          print(f"C2: {C2}")
          k2 = list_xor([K[i] for i in C2])
          print(f"k2: {k2}")
          print(f"k2_len: {len(k2)}")
          print(f"str(t1).encode_len: {len(str(t1).encode())}")
          xor_result = xor(k2, str(t1).encode())
          print(f"xor_result: {xor_result}")

          t2 = random.randint(0, 255)
          payload_M4 = f"{r2}#{t2}"
          print(f"payload: {payload_M4}")
          M4 = encrypt(xor_result, payload_M4.encode())
          print(f"M4: {M4}")





if __name__ == "__main__":
    main()
