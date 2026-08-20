import json


class Request:
    def __init__(self, plain_text):
        self.header, self.body = self._separate_body(plain_text)
        self.method, self.path, self.raw_query = self._process_line(self.header)
        self.headers = self._process_header(self.header)
        self.json = self._create_json()
        self.query = self._separate_query()

    def _separate_body(self, text):
        elements = text.split("\r\n\r\n")
        header = elements[0]
        body = elements[1] if len(elements) > 1 else ""
        return header, body

    def _process_line(self, header):
        lines = header.splitlines()
        if not lines:
            return None, None, None

        first_line = lines[0].strip()
        parts = first_line.split()

        if len(parts) < 2:
            return None, None, None

        method = parts[0]
        path = parts[1]
        query = ""

        if "?" in path:
            query = path.split("?", 1)[1]
            path = path.split("?", 1)[0]

        if path != "/":
            path = path.rstrip("/")

        return method, path, query

    def _process_header(self, header):
        lines = header.splitlines()
        headers = {}
        for line in lines[1:]:
            if ":" not in line:
                continue
            clave, valor = line.split(":", 1)
            headers[clave.strip()] = valor.strip()
        return headers

    def _create_json(self):
        body_json = {}
        if self.body:
            try:
                body_json = json.loads(self.body)
            except json.JSONDecodeError as e:
                return {}
        return body_json

    def _separate_query(self):
        query = str(self.raw_query)
        dict_query = {}

        if query:
            list_query = query.split("&")
            for item in list_query:
                if "=" in item:
                    key, value = item.split("=", 1)
                    dict_query[key] = value
                else:
                    dict_query[item] = "true"
        return dict_query


if __name__ == "__main__":
    plain = """POST /productos/?notificar=true&almacen=centro HTTP/1.1\r\nHost: ://tienda.com\r\nContent-Type: application/json\r\nContent-Length: 95\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\n\r\n{\n  "nombre": "Teclado Mecánico RGB",\n  "precio": 79.99,\n  "stock": 45,\n  "categoria": "perifericos"\n}"""

    request = Request(plain)

    print(request.query)
    print(request.path)
