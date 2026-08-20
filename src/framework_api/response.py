from datetime import datetime, timezone
import json

class HTTPResponse():

    def __init__(self,status_code,content_type,Body_bytes):

        self.status_code = status_code
        self.content_type = content_type
        self.body_bytes = Body_bytes
        self.headers = {}

    def _formated_header(self):

        actual_date = datetime.now(timezone.utc)
        formated_date = actual_date.strftime("%a, %d %b %Y %H:%M:%S GMT")

        header = f"HTTP/1.1 {self.status_code}\r\n"
        header += f"Content-Type: {self.content_type}\r\n"
        header += f"Content-Length: {len(self.body_bytes)}\r\n"
        header += "Connection: close\r\n"

        for key, value in self.headers.items():
            header += f"{key}: {value}\r\n"

        header += "\r\n"
        return header

    def export_bytes(self) -> bytes:
        header = self._formated_header()
        header_bytes = header.encode("utf-8")
        return header_bytes + self.body_bytes 

    @classmethod
    def json(cls,status_code,body_data):
        json_data = json.dumps(body_data)
        json_bytes = json_data.encode("utf-8")
        content = "application/json; charset=utf-8"

        return cls(status_code,content,json_bytes)