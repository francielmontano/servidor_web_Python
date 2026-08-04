import re
from .response import HTTPResponse

class Router():

    def __init__(self,public_dir):
        self.public_dir = public_dir 
        self.routes = {"GET": [], "POST": [], "PUT": [], "DELETE": []}
        self.extensions = {".html": "text/html; charset=utf-8", 
                           ".css": "text/css; charset=utf-8", 
                           ".js": "application/javascript; charset=utf-8",
                           ".png": "image/png",
                           ".jpg": "image/jpeg",
                           ".ico": "image/x-icon"}


    def _convert_regex(self,path):
        pattern = re.sub(r'<[^>]+>', r'([^/]+)', path)
        return re.compile(f"^{pattern}$")

    def get(self, path):
        def decorate(func):
            regex_pattern = self._convert_regex(path)
            self.routes["GET"].append((regex_pattern,func))
            return func
        return decorate

    def post(self, path):
        def decorate(func):
            regex_pattern = self._convert_regex(path)
            self.routes["POST"].append((regex_pattern,func))
            return func
        return decorate

    def put(self,path):
        def decorate(func):
            regex_pattern = self._convert_regex(path)
            self.routes["PUT"].append((regex_pattern))
            return func
        return decorate

    def delete(self,path):
        def decorate(func):
            regex_pattern =self._convert_regex(path)
            self.routes["DELETE"].append((regex_pattern))
            return func
        return decorate



    def include_router(self,sub_router, prefix=""):
        for metod , tuple_list in sub_router.routes.items():
            for regex_pattern, func in tuple_list:
                path_original = regex_pattern.pattern.lstrip('^').rstrip('$')
                mix_path = prefix + path_original
                new_regex = self._convert_regex(mix_path)

                self.routes[metod].append((new_regex, func))

    def resolve(self, method, request_object):

        request_path = request_object.path

        # Buscar rutas registradas
        if method in self.routes:

            print("Método recibido:", method)
            print("Rutas registradas:")

            for regex_pattern, func in self.routes[method]:
                coincidence = regex_pattern.match(request_path)

                if coincidence:
                    variables = coincidence.groups()
                    return func(request_object, *variables)

        if method == "GET":

            file = "index.html" if request_path == "/" else request_path.lstrip("/")

            file_path = self.public_dir / file

            if file_path.exists() and file_path.is_file():

                content_type = self.extensions.get(
                    file_path.suffix,
                    "application/octet-stream"
                )

                return HTTPResponse(
                    "200 OK",
                    content_type,
                    file_path.read_bytes()
                )

        body = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>404 - No encontrado</title>
        </head>
        <body>
            <h1>404 - Recurso no encontrado</h1>
            <p>No existe la ruta:</p>
            <code>{request_path}</code>
        </body>
        </html>
        """

        return HTTPResponse(
            "404 Not Found",
            "text/html; charset=utf-8",
            body.encode("utf-8")
        )
    