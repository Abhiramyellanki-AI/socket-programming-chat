import socket

HOST = "127.0.0.1"
PORT = 5001
MAX_CLIENTS = 2

clients = set()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))

    print(f"UDP server running on {HOST}:{PORT}")
    print(f"Waiting for {MAX_CLIENTS} clients...")

    try:
        while True:
            data, address = server.recvfrom(1024)
            message = data.decode("utf-8").strip()

            if message == "JOIN":
                if address in clients:
                    server.sendto(
                        b"You are already in the chat.",
                        address,
                    )
                    continue

                if len(clients) >= MAX_CLIENTS:
                    server.sendto(
                        b"Chat is full. Try again later.",
                        address,
                    )
                    continue

                clients.add(address)
                print(f"[CONNECTED] {address}")

                server.sendto(
                    b"Welcome! You joined the UDP chat.",
                    address,
                )
                continue

            if message == "EXIT":
                if address in clients:
                    clients.remove(address)
                    print(f"[DISCONNECTED] {address}")

                server.sendto(b"Goodbye!", address)
                continue

            if address not in clients:
                server.sendto(
                    b"Please join the chat first.",
                    address,
                )
                continue

            print(f"[{address}] {message}")

            outgoing = (
                f"Client {address[1]}: {message}"
            ).encode("utf-8")

            for recipient in list(clients):
                if recipient != address:
                    server.sendto(outgoing, recipient)

    except KeyboardInterrupt:
        print("\nShutting down UDP server.")

    finally:
        server.close()


if __name__ == "__main__":
    main()
