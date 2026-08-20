from framework_api.request import Request
from framework_api.response import HTTPResponse
import threading, socket
import traceback

class HTTPServer():

    def __init__(self,router,host="127.0.0.1",port=8080):
        self.router = router
        self.host = host
        self. port = port 

    def start(self):

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host,self.port))
        server.listen(5)

           
        while True:
            try:
                client_socket, client_address = server.accept()
                print(f"[CONEXIÓN] Cliente desde: {client_address[0]}:{client_address[1]}")
                client_socket.settimeout(10)
                hilo = (threading.Thread(target=self.atender_cliente, args=(client_socket,)))
                hilo.start()
            except Exception as e:
                traceback.print_exc()
                continue

    def atender_cliente(self, socket_client):
        try:
            print("Esperando datos...")
            bytes_recibidos = socket_client.recv(4096)
            print("Datos recibidos")

            if not bytes_recibidos:
                return

            plain_text = bytes_recibidos.decode("utf-8")
            request = Request(plain_text)
            plain_text = bytes_recibidos.decode("utf-8")
            response = self.router.resolve(request.method, request)

            if response is None:
                response = HTTPResponse(
                    "404 Not Found",
                    "text/html",
                    b"<h1>404 Not Found</h1>"
                )

            socket_client.sendall(response.export_bytes())

        except socket.timeout:
            print("[TIMEOUT] Cliente inactivo.")

        except Exception:
            traceback.print_exc()

            try:
                error = HTTPResponse(
                    "500 Internal Server Error",
                    "text/html",
                    b"<h1>500 Internal Server Error</h1>"
                )

                socket_client.sendall(error.export_bytes())

            except Exception:
                pass

        finally:
            socket_client.close()

            
