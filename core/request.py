class Request():
    def __init__(self, plain_text):
        self.header, self.body = self._separate_body(plain_text)
        self.method, self.path = self._process_line(self.header)
        self.headers = self._process_header(self.header)

    def _separate_body(self, text):
        elements = text.split("\r\n\r\n")
        header = elements[0]
        # Corregido: Validar si realmente existe un cuerpo en la petición
        body = elements[1] if len(elements) > 1 else ""
        return header, body

    def _process_line(self, header):
        # Usamos splitlines() que es más seguro para manejar saltos de línea de red
        lines = header.splitlines()
        if not lines:
            return None, None
            
        first_line = lines[0].strip()
        parts = first_line.split()

        if len(parts) >= 2:
            return parts[0], parts[1]
        return None, None

    def _process_header(self, header):
        lines = header.splitlines()
        headers = {}
        for line in lines[1:]: # Omitimos la primera línea (GET / ...)
            if ":" not in line:
                continue
            clave, valor = line.split(":", 1)
            headers[clave.strip()] = valor.strip()
        return headers

