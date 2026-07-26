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
        
        peticion = ""
        try:
            peticion = client_socket.recv(1024).decode('utf-8')
        except (socket.timeout, ConnectionResetError):
            pass

        if peticion and len(peticion.strip()) > 0:
            primera_linea = peticion.split('\n')[0]
            partes = primera_linea.split(' ')

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

        ruta_archivo = Path("public/" + archivo)

        extencions = {
            ".html": "text/html",
            ".css": "text/css",
            ".js": "application/javascript",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".ico": "image/x-icon"
        }

        if ruta_archivo.exists() and ruta_archivo.is_file():
            extension = ruta_archivo.suffix

            tipo_contenido = extencions.get(extension,"text/plain")
            codigo_estado = "200 OK"
            contenido = ruta_archivo.read_bytes()
            

        cabecera = (
            f"HTTP/1.1 {codigo_estado}\r\n"
            f"Content-Type: {tipo_contenido}; charset=utf-8\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode("utf-8")

        try:
            client_socket.sendall(cabecera + contenido)
        except Exception:
            pass
        finally:
            client_socket.close()
            print("[CONEXIÓN CERRADA]\n")

except KeyboardInterrupt:
    print("\n[APAGADO] Servidor detenido por el usuario de forma segura.")
finally:
    server.close()
