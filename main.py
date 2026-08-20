from pathlib import Path
import json
from datetime import datetime

from src.core import Router, HTTPServer, HTTPResponse

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"

router = Router(PUBLIC_DIR)


@router.get("/h")
def hola(request):

    return "Hola desde tu framework."


@router.get("/time")
def hora(request):

    return str(datetime.now())


@router.get("/json")
def json_endpoint(request):

    data = {"framework": "MiniHTTP", "version": "1.0", "status": "running"}

    return data


@router.get("/usuario/<nombre>")
def usuario(request, nombre):

    html = f"""
    <h1>Bienvenido {nombre}</h1>
    """

    return HTTPResponse("200 OK", "text/html", html.encode())


@router.get("/suma/<a>/<b>")
def suma(request, a, b):

    total = int(a) + int(b)

    return total


@router.get("/headers")
def headers(request):

    response = HTTPResponse("200 OK", "text/plain", b"Cabeceras personalizadas.")

    response.headers["X-Framework"] = "MiniHTTP"

    response.headers["X-Version"] = "1.0"

    response.headers["X-Creador"] = "Franciel"

    return response


@router.get("/estado/<codigo>")
def estado(request, codigo):

    estados = {
        "200": "200 OK",
        "201": "201 Created",
        "400": "400 Bad Request",
        "401": "401 Unauthorized",
        "403": "403 Forbidden",
        "500": "500 Internal Server Error",
    }

    status = estados.get(codigo)

    if status is None:

        return HTTPResponse("404 Not Found", "text/plain", b"Codigo HTTP desconocido.")

    return status


@router.get("/error")
def error(request):

    raise RuntimeError("Error de prueba.")


@router.post("/usuarios")
def crear_usuario(request):

    print("========== NUEVO POST ==========")
    print("Método :", request.method)
    print("Ruta   :", request.path)
    print("Headers:", request.headers)
    print("Body   :", request.body)
    print("===============================")

    body = f"""
<!DOCTYPE html>
<html>
<head>
    <title>POST recibido</title>
</head>
<body>

<h1>POST recibido correctamente</h1>

<h2>Información</h2>

<p><strong>Método:</strong> {request.method}</p>

<p><strong>Ruta:</strong> {request.path}</p>

<h3>Body</h3>

<pre>{request.body}</pre>

</body>
</html>
"""

    response = HTTPResponse(
        "201 Created", "text/html; charset=utf-8", body.encode("utf-8")
    )

    response.headers["X-Framework"] = "MiniHTTP"

    return response


import json


@router.post("/debug")
def debug(request):

    data = {
        "method": request.method,
        "path": request.path,
        "headers": request.headers,
        "body": request.body,
    }

    return data


@router.post("/descargar/<ruta>")
def descargar_reporte(request, ruta):

    ruta = Path(f"public/{ruta}")
    content_type = router.extensions.get(ruta.suffix, "application/octet-stream")

    try:
        with open(ruta, "rb") as f:
            contenido = f.read()
    except FileNotFoundError:
        # Si no encuentra el archivo, puedes retornar un error de prueba
        return HTTPResponse(
            "404 Not Found", "text/plain", b"Archivo no encontrado en el servidor"
        )

    response = HTTPResponse(
        "200 OK", content_type, contenido  # Indica que es un archivo PDF
    )

    # Este header es el secreto para que el navegador lo descargue en vez de abrirlo
    response.headers["Content-Disposition"] = (
        f'attachment; filename="{ruta.stem}{ruta.suffix}"'
    )

    return response


@router.get("/type_error")
def erro_500():
    return []


if __name__ == "__main__":

    host = "100.66.137.85"
    port = 8085

    print("=" * 50)
    print("Mini HTTP Framework")
    print(f"Escuchando en http://{host}:{port}")
    print("=" * 50)

    server = HTTPServer(router=router, host=host, port=port)

    server.start()
