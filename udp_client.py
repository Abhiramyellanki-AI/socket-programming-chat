
import socket
import threading

HOST = "127.0.0.1"
PORT = 5001

running = threading.Event()


def receive_messages(client):
    """Receive messages from the UDP server."""
    while running.is_set():
        try:
            data, _ = client.recvfrom(1024)
            print(f"\n{data.decode('utf-8')}", flush=True)

            if data == b"Goodbye!":
                running.clear()
                break

        except socket.timeout:
            continue

        except OSError:
            break


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(1.0)

    running.set()

    try:
        client.sendto(b"JOIN", (HOST, PORT))
        print("Joining the UDP chat...")
        print("Type a message and press Enter. Type 'exit' to leave.")

        receiver = threading.Thread(
            target=receive_messages,
            args=(client,),
            daemon=True,
        )
        receiver.start()

        while running.is_set():
            try:
                message = input()

            except (EOFError, KeyboardInterrupt):
                message = "exit"

            if message.strip().lower() == "exit":
                client.sendto(b"EXIT", (HOST, PORT))
                running.clear()
                break

            client.sendto(message.encode("utf-8"), (HOST, PORT))

    except OSError as error:
        print(f"UDP client error: {error}")

    finally:
        running.clear()
        client.close()
        print("UDP client closed.")


if __name__ == "__main__":
    main()
