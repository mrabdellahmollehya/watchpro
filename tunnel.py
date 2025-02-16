import paramiko
import socket
import threading

def forward_tunnel(local_port, remote_host, remote_port, ssh_host, ssh_port, ssh_user, ssh_pass):
    # Connect to the SSH server
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ssh_host, ssh_port, ssh_user, ssh_pass)
        print("Connected to SSH server")
    except Exception as e:
        print(f"SSH connection failed: {e}")
        return

    # Set up local socket listener
    local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        local_socket.bind(('0.0.0.0', local_port))
    except PermissionError:
        print("Error: Permission denied. Try running with sudo.")
        client.close()
        return
    local_socket.listen(5)
    print(f"Listening on port {local_port}. Forwarding to {remote_host}:{remote_port} via SSH")

    try:
        while True:
            client_sock, client_addr = local_socket.accept()
            print(f"Incoming connection from {client_addr}")
            thread = threading.Thread(target=handle_client, args=(client_sock, client, remote_host, remote_port))
            thread.start()
    except KeyboardInterrupt:
        print("Shutting down...")
        local_socket.close()
        client.close()

def handle_client(client_sock, ssh_client, remote_host, remote_port):
    try:
        # Open SSH channel to remote host
        transport = ssh_client.get_transport()
        chan = transport.open_channel('direct-tcpip', (remote_host, remote_port), client_sock.getpeername())
    except Exception as e:
        print(f"Channel error: {e}")
        client_sock.close()
        return

    if not chan:
        print("Channel setup failed")
        client_sock.close()
        return

    print(f"Tunnel established {client_sock.getpeername()} -> {remote_host}:{remote_port}")

    # Bidirectional forwarding
    def forward(source, dest, direction):
        try:
            while True:
                data = source.recv(1024)
                if not data:
                    break
                dest.send(data)
        except Exception as e:
            pass  # Connection closed
        finally:
            source.close()
            dest.close()

    # Start forwarding threads
    client_to_remote = threading.Thread(target=forward, args=(client_sock, chan, "->"))
    remote_to_client = threading.Thread(target=forward, args=(chan, client_sock, "<-"))
    client_to_remote.start()
    remote_to_client.start()

    # Wait for threads to complete
    client_to_remote.join()
    remote_to_client.join()
    print("Tunnel closed")

if __name__ == '__main__':
    forward_tunnel(
        local_port=3389,
        remote_host='127.0.0.1',  # Forward to SSH server's own 3389 port
        remote_port=3389,
        ssh_host='provide-documents.gl.at.ply.gg',
        ssh_port=31642,
        ssh_user='runner',
        ssh_pass='123456a'
  )
