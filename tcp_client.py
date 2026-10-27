import socket
import threading

HOST = "127.0.0.1"
PORT = 5000


def receive_messages(client):
    """Listen for messages from the server."""
    while True:
        try:
            data = client.recv(1024)

            if not data:
                print("\nServer disconnected.")
                break

            print(data.decode("utf-8"), end="", flush=True)

        except OSError:
            break


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print("Connected to the TCP chat server.")
        print("Type a message and press Enter. Type 'exit' to leave.")

        receiver = threading.Thread(
            target=receive_messages,
            args=(client,),
            daemon=True,
        )
        receiver.start()

        while True:
            message = input()

            try:
                client.sendall((message + "\n").encode("utf-8"))
            except OSError:
                print("Connection to the server was lost.")
                break

            if message.strip().lower() == "exit":
                break

    except ConnectionRefusedError:
        print("Could not connect. Start tcp_server.py first.")

    except OSError as error:
        print(f"Connection error: {error}")

    finally:
        client.close()
        print("TCP client closed.")


if __name__ == "__main__":
    main()
