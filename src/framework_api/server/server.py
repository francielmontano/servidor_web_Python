from ..my_http import HTTPResponse, Request
from ..my_logging.loging import Logger
import threading, socket, traceback

class HTTPServer:
    
    

    def __init__(self, router, host="127.0.0.1", port=8080):
        self.router = router
        self.host = host
        self.port = port
        self.write_log = Logger(20,"HTTPServer")

    def start(self):

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)

        while True:
            try:
                client_socket, client_address = server.accept()
                self.write_log.info(f"[CONEXIÓN] Cliente desde: {client_address[0]}:{client_address[1]}")
                
                hilo = threading.Thread(
                    target=self.atender_cliente, args=(client_socket,)
                )
                hilo.start()
            except Exception as e:
                traceback.print_exc()
                continue

    def atender_cliente(self, socket_client):

        socket_client.settimeout(4.0)
        try:
            while True:
                try:
                    self.write_log.info("[CONEXIÓN] Esperando datos del cliente...")
                    bytes_recibidos = socket_client.recv(4096)
                    self.write_log.info("[CONEXIÓN] Datos recibidos.")

                    if not bytes_recibidos:
                        break

                    plain_text = bytes_recibidos.decode("utf-8")
                    request = Request(plain_text)
                    plain_text = bytes_recibidos.decode("utf-8")
                    response = self.router.resolve(request.method, request)

                    if response is None:
                        response = HTTPResponse(
                            "404 Not Found", "text/html", b"<h1>404 Not Found</h1>"
                        )
                        
                    response.headers["connection"] = "keep-alive"
                    socket_client.sendall(response.export_bytes())

                except socket.timeout:
                    self.write_log.warning("[TIMEOUT] Cliente inactivo.")
                    break

                except Exception:
                    traceback.print_exc()

                    try:
                        error = HTTPResponse(
                            "500 Internal Server Error",
                            "text/html",
                            b"<h1>500 Internal Server Error</h1>",
                        )
                        error.headers["connection"] = "close"
                        socket_client.sendall(error.export_bytes())

                    except Exception:
                        pass
                    break

        finally:
            self.write_log.info("[CONEXIÓN] Cerrando conexión con el cliente.")
            socket_client.close()
