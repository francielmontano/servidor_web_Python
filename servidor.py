import socket
from pathlib import Path

# Configuración inicial del servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 8080))
server.listen(5)
print("Servidor HTTP activo en http://localhost:8080 ...")
print("Presiona Ctrl + C para apagar el servidor de forma segura.\n")

try:
    while True: 
        client_socket, client_address = server.accept()
        print(f"[CONEXIÓN] Cliente desde: {client_address[0]}:{client_address[1]}")
        
        client_socket.settimeout(0.2)
        
        request = ""
        try:
            request = client_socket.recv(1024).decode('utf-8')
        except (socket.timeout, ConnectionResetError):
            pass

        if request and len(request.strip()) > 0:
            first_part = request.split('\n')[0]
            partes = first_part.split(' ')

            if len(partes) > 1:
                ruta = partes[1]
            else:
                ruta = "/"
        else:
            ruta = "/"

        print(f"Ruta solicitada: {ruta}")

        if ruta == "/":
            archivo = "index.html"
        else:
            archivo = ruta.lstrip("/")

        file_path = Path("public/" + archivo)

        extencions = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".ico": "image/x-icon"
        }

        content_type = "text/html"
        status_code = "404 Not Found"
        content = b"<h1>404 Page Not Found</h1>"

        if file_path.exists() and file_path.is_file():
            extension = file_path.suffix

            content_type = extencions.get(extension,"text/plain")
            status_code = "200 OK"
            content = file_path.read_bytes()
            

        head = (
            f"HTTP/1.1 {status_code}\r\n"
            f"Content-Type: {content_type}"
            "Connection: close\r\n"
            "\r\n"
        ).encode("utf-8")

        try:
            client_socket.sendall(head + content)
        except Exception:
            pass
        finally:
            client_socket.close()
            print("[CONEXIÓN CERRADA]\n")

except KeyboardInterrupt:
    print("\n[APAGADO] Servidor detenido por el usuario de forma segura.")
finally:
    server.close()
