import os
import socket
import ssl

# SMTP Protocol Implementation
class SMTPProtocol:
    def __init__(self):
        self.state = "INIT"
        self.sender = None
        self.recipients = []
        self.data = []

    def handle_command(self, command):
        cmd = command.split(" ", 1)
        command = cmd[0].upper()

        if command == "HELO":
            return self.handle_helo(cmd)
        elif command == "MAIL":
            return self.handle_mail_from(cmd)
        elif command == "RCPT":
            return self.handle_rcpt_to(cmd)
        elif command == "DATA":
            return self.handle_data(cmd)
        elif command == "QUIT":
            return self.handle_quit(cmd)
        else:
            return "500 Command not recognized"

    def handle_helo(self, cmd):
        if len(cmd) < 2:
            return "501 Syntax error in parameters"
        self.state = "HELO"
        return f"250 Hello {cmd[1]}"

    def handle_mail_from(self, cmd):
        if self.state != "HELO" or len(cmd) < 2 or not cmd[1].startswith("FROM:"):
            return "503 Bad sequence of commands"
        self.sender = cmd[1][5:].strip()
        return "250 OK"

    def handle_rcpt_to(self, cmd):
        if not self.sender or len(cmd) < 2 or not cmd[1].startswith("TO:"):
            return "503 Bad sequence of commands"
        self.recipients.append(cmd[1][3:].strip())
        return "250 OK"

    def handle_data(self, cmd):
        self.state = "DATA"
        return "354 End data with <CR><LF>.<CR><LF>"

    def handle_quit(self, cmd):
        return "221 Bye"

    def handle_data_lines(self, lines):
        self.data = lines
        self.state = "INIT"
        return "250 Message received"


# Email Storage
class EmailStorage:
    def __init__(self, storage_dir="emails"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save_email(self, sender, recipients, data):
        email_id = len(os.listdir(self.storage_dir)) + 1
        email_path = os.path.join(self.storage_dir, f"email_{email_id}.txt")
        with open(email_path, "w") as f:
            f.write(f"From: {sender}\n")
            f.write(f"To: {', '.join(recipients)}\n")
            f.write("\n".join(data))
        return email_path


# Connection Handling
class SMTPServer:
    def __init__(self, host="0.0.0.0", port=8025, use_tls=False):
        self.host = host
        self.port = port
        self.use_tls = use_tls
        self.storage = EmailStorage()

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"SMTP server listening on {self.host}:{self.port}")
        while True:
            client_socket, address = server_socket.accept()
            print(f"Connection from {address}")
            self.handle_client(client_socket)

    def handle_client(self, client_socket):
        protocol = SMTPProtocol()
        client_socket.send(b"220 Welcome to SMTP Server\r\n")

        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break

                data = data.decode(errors="replace").strip()
                print(f"Received Command: '{data}'")

                if protocol.state == "DATA":
                    if data == ".":
                        response = protocol.handle_data_lines(protocol.data)
                        self.storage.save_email(protocol.sender, protocol.recipients, protocol.data)
                    else:
                        protocol.data.append(data)
                        continue
                else:
                    response = protocol.handle_command(data)

                print(f"Response: {response}")
                client_socket.send((response + "\r\n").encode())

                if response.startswith("221"):
                    break

            except Exception as e:
                print(f"Error: {e}")
                client_socket.send(b"500 Internal Server Error\r\n")
                break

        client_socket.close()


if __name__ == "__main__":
    server = SMTPServer(host="0.0.0.0", port=8025, use_tls=False)
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("Server shutting down.")
