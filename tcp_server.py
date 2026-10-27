import socket
import threading

HOST = "127.0.0.1"
PORT = 5000
MAX_CLIENTS = 2

clients = []
clients_lock = threading.Lock()


def broadcast(message, sender):
    """Forward a message to every client except its sender."""
    with clients_lock:
        recipients = [client for client in clients if client != sender]

    for client in recipients:
        try:
            client.sendall(message)
        except OSError:
            remove_client(client)


def remove_client(client):
    """Remove a disconnected client safely."""
    with clients_lock:
        if client in clients:
            clients.remove(client)

    try:
        client.close()
    except OSError:
        pass


def handle_client(client, address):
    print(f"[CONNECTED] {address}")

    try:
        client.sendall(
            b"Welcome! You are connected to the TCP chat server.\n"
        )

        while True:
            data = client.recv(1024)

            if not data:
                break

            message = data.decode("utf-8").strip()

            if message.lower() == "exit":
                break

            print(f"[{address}] {message}")

            broadcast(
                f"Client {address[1]}: {message}\n".encode("utf-8"),
                client,
            )

    except (ConnectionError, OSError) as error:
        print(f"[ERROR] {address}: {error}")

    finally:
        print(f"[DISCONNECTED] {address}")
        remove_client(client)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((HOST, PORT))
        server.listen(MAX_CLIENTS)

        print(f"TCP server running on {HOST}:{PORT}")
        print(f"Waiting for {MAX_CLIENTS} clients...")

        while True:
            client, address = server.accept()

            with clients_lock:
                if len(clients) >= MAX_CLIENTS:
                    client.sendall(b"Chat is full. Try again later.\n")
                    client.close()
                    continue

                clients.append(client)

            thread = threading.Thread(
                target=handle_client,
                args=(client, address),
                daemon=True,
            )
            thread.start()

    except KeyboardInterrupt:
        print("\nShutting down TCP server.")

    finally:
        with clients_lock:
            connected_clients = clients.copy()
            clients.clear()

        for client in connected_clients:
            try:
                client.close()
            except OSError:
                pass

        server.close()


if __name__ == "__main__":
    main()
