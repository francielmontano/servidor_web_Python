from abc import ABC, abstractmethod
from .response import HTTPResponse
from types import NoneType


class TypeResponse(ABC):
    @abstractmethod
    def response(self, result: str) -> None:
        pass


class ResponseType(TypeResponse):
    def response(self, result) -> HTTPResponse:
        return result


class JsonType(TypeResponse):
    def response(self, result):
        return HTTPResponse.json("200 OK", result)


class StringType(TypeResponse):
    def response(self, result):
        return HTTPResponse(
            "200 OK", "text/plain; charset=utf-8", result.encode("utf-8")
        )


class Request_type:

    _type_map = {HTTPResponse: ResponseType, str: StringType}

    json_archives = [dict, list, tuple, int, float, bool, NoneType]

    _type_map.update(dict.fromkeys(json_archives, JsonType))

    @classmethod
    def reponse_auto(cls, tipo):
        type_response = cls._type_map.get(type(tipo))
        print(type_response)
        if not type_response:
            return HTTPResponse(
                "500 Internal Server Error",
                "text/html; charset=utf-8",
                b"<h1>500 Internal Server Error</h1>",
            )
        return type_response()
