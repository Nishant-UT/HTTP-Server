import socket
import os
import gzip
import threading
import zlib

HOST = "localhost"
PORT = 9999
WEB_ROOT = "public"  # Directory for static files

def compress_data(data, encoding):
    """Compress data based on the requested encoding."""
    if encoding == "gzip":
        return gzip.compress(data)
    elif encoding == "deflate":
        return zlib.compress(data)
    return data  # No compression

def parse_headers(header_lines):
    """Parse HTTP headers into a dictionary."""
    headers = {}
    for line in header_lines:
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key.lower()] = value
    return headers

def handle_client(client_socket):
    """Handle a single client connection."""
    try:
        request_data = client_socket.recv(4096).decode()
        if not request_data:
            client_socket.close()
            return

        print("Received request:\n", request_data)

        # Extract request line & headers
        request_lines = request_data.split("\r\n")
        request_line = request_lines[0]  # First line of the request
        headers = parse_headers(request_lines[1:])  # Remaining lines

        # Parse request line (e.g., "GET /index.html HTTP/1.1")
        parts = request_line.split(" ")
        if len(parts) < 3:
            response = "HTTP/1.1 400 Bad Request\r\n\r\n"
            client_socket.sendall(response.encode())
            client_socket.close()
            return

        method, path, _ = parts[0], parts[1], parts[2]

        # Default response
        status_line = "HTTP/1.1 404 Not Found\r\n"
        response_body = "404 Not Found".encode()

        # Handle GET requests
        if method == "GET":
            file_path = os.path.join(WEB_ROOT, path.strip("/"))
            if os.path.exists(file_path) and os.path.isfile(file_path):
                with open(file_path, "rb") as f:
                    response_body = f.read()
                status_line = "HTTP/1.1 200 OK\r\n"
            elif path == "/":
                status_line = "HTTP/1.1 200 OK\r\n"
                response_body = "Hello, world!".encode()

        # Handle POST requests
        elif method == "POST":
            content_length = int(headers.get("content-length", 0))
            request_body = client_socket.recv(content_length).decode() if content_length > 0 else ""
            print(f"Received POST body:\n{request_body}")
            status_line = "HTTP/1.1 200 OK\r\n"
            response_body = f"Received Data: {request_body}".encode()

        # Reject unsupported methods
        else:
            status_line = "HTTP/1.1 405 Method Not Allowed\r\n"
            response_body = "405 Method Not Allowed".encode()

        # Handle Compression
        accept_encoding = headers.get("accept-encoding", "")
        if "gzip" in accept_encoding:
            response_body = compress_data(response_body, "gzip")
            status_line += "Content-Encoding: gzip\r\n"
        elif "deflate" in accept_encoding:
            response_body = compress_data(response_body, "deflate")
            status_line += "Content-Encoding: deflate\r\n"

        # Construct and send response
        response = f"{status_line}\r\n"
        client_socket.sendall(response.encode() + response_body)

    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        client_socket.close()

def main():
    """Main function to start the HTTP server."""
    print(f"Starting server on {HOST}:{PORT}...")

    server_socket = socket.create_server((HOST, PORT))
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.listen(5)

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()  # Handle clients concurrently

if __name__ == "__main__":
    main()
