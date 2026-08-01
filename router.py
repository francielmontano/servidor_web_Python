from pathlib import Path 


class Router():

    def __init__(self,public_dir="public"):

        self.public_dir = public_dir
        self.routes = {
            "GET": {},
            "POST": {},
            "PUT": {},
            "DELETE": {}
        }




