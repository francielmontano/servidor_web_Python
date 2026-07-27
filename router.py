from controllers import manage_static

def route_request(path: str):

    real_path = path.split(" ")[1].lstrip("/")

    status, data_type, content = manage_static(real_path)

    return status, data_type, content


