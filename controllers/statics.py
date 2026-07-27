from pathlib import Path 
import mimetypes

def manage_static(clean_path):

    file_path = Path("public") / clean_path

    if file_path.exists() and file_path.is_file(): 
        status = "200 OK"
        data_type = mimetypes.guess_type(str(file_path))
        content = clean_path.read_bytes()
    else: 
        status = "404 Not Found"
        data_type = "text/html"
        content = b"<h1>4040 Not Found</h1>"

    return status, data_type, content

   

    