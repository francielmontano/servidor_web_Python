from pathlib import Path
import json
from datetime import datetime

from core import Router, HTTPServer, HTTPResponse

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"

router = Router(public_dir=PUBLIC_DIR)

@router.get("/page2")
def home(request):

    html = f"""
    <html>
        <head>
            <title>Mini Framework</title>
        </head>

        <body>

            <h1>🚀 Mini HTTP Framework</h1>

            <p>Servidor funcionando correctamente.</p>

            <hr>

            <ul>
                <li><a href="/hola">Hola</a></li>
                <li><a href="/time">Hora</a></li>
                <li><a href="/headers">Headers</a></li>
                <li><a href="/json">JSON</a></li>
                <li><a href="/usuario/Franciel">Usuario</a></li>
                <li><a href="/suma/20/35">Suma</a></li>
                <li><a href="/estado/403">Estado HTTP</a></li>
                <li><a href="/error">Error</a></li>
            </ul>

        </body>
    </html>
    """

    return HTTPResponse(
        "200 OK",
        "text/html; charset=utf-8",
        html.encode()
    )

@router.get("/hola")
def hola(request):

    return HTTPResponse(
        "200 OK",
        "text/plain",
        b"Hola desde tu framework."
    )


@router.get("/time")
def hora(request):

    return HTTPResponse(
        "200 OK",
        "text/plain",
        str(datetime.now()).encode()
    )

@router.get("/json")
def json_endpoint(request):

    data = {
        "framework": "MiniHTTP",
        "version": "1.0",
        "status": "running"
    }

    return HTTPResponse(
        "200 OK",
        "application/json",
        json.dumps(data).encode()
    )

@router.get("/usuario/<nombre>")
def usuario(request, nombre):

    html = f"""
    <h1>Bienvenido {nombre}</h1>
    """

    return HTTPResponse(
        "200 OK",
        "text/html",
        html.encode()
    )


@router.get("/suma/<a>/<b>")
def suma(request, a, b):

    total = int(a) + int(b)

    return HTTPResponse(
        "200 OK",
        "text/plain",
        f"{a} + {b} = {total}".encode()
    )

@router.get("/headers")
def headers(request):

    response = HTTPResponse(
        "200 OK",
        "text/plain",
        b"Cabeceras personalizadas."
    )

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
        "500": "500 Internal Server Error"
    }

    status = estados.get(codigo)

    if status is None:

        return HTTPResponse(
            "404 Not Found",
            "text/plain",
            b"Codigo HTTP desconocido."
        )

    return HTTPResponse(
        status,
        "text/plain",
        status.encode()
    )

@router.get("/error")
def error(request):

    raise RuntimeError("Error de prueba.")

@router.get("/download")
def download(request):

    archivo = PUBLIC_DIR / "index.html"

    response = HTTPResponse(
        "200 OK",
        "text/html",
        archivo.read_bytes()
    )

    response.headers["Content-Disposition"] = 'attachment; filename="index.html"'

    return response


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
        "201 Created",
        "text/html; charset=utf-8",
        body.encode("utf-8")
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
        "body": request.body
    }

    return HTTPResponse(
        "200 OK",
        "application/json",
        json.dumps(data, indent=4).encode()
    )

@router.post("/descargar")
def descargar_reporte(request):
    try:
        with open("public/images/html.png", "rb") as f:
            contenido = f.read()
    except FileNotFoundError:
        # Si no encuentra el archivo, puedes retornar un error de prueba
        return HTTPResponse("404 Not Found", "text/plain", b"Archivo no encontrado en el servidor")

    response = HTTPResponse(
        "200 OK",
        "application/pdf",  # Indica que es un archivo PDF
        contenido
    )
    
    # Este header es el secreto para que el navegador lo descargue en vez de abrirlo
    response.headers["Content-Disposition"] = 'attachment; filename="imagen.png"'
    
    return response


if __name__ == "__main__":

    host = "100.66.137.85"
    port = 8085

    print("=" * 50)
    print("Mini HTTP Framework")
    print(f"Escuchando en http://{host}:{port}")
    print("=" * 50)

    server = HTTPServer(
        router=router,
        host= host,
        port= port
    )

    server.start()