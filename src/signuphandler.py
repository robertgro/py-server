import json

class SignupHandler:
    def __init__(self, *args, **kwargs):
        pass
    
    def handleSignupPOST(self, requestHandler):
        content_length = requestHandler.headers.get("Content-Length")
        if content_length is None:
            requestHandler.send_response(400, "Bad Request")
            requestHandler.end_headers()
            return
        post_body = requestHandler.rfile.read(int(content_length))
        #print(post_body.decode("utf-8"))
        try:
            json_object = json.loads(post_body.decode("utf-8"))
        except json.decoder.JSONDecodeError as e:
            print("json.decoder.JSONDecodeError", e)
            requestHandler.send_response(415, "Unsupported Media Type")
            requestHandler.end_headers()
            requestHandler.wfile.write(b"Error: unsupported media type")
            return
        requestHandler.send_response(200)
        requestHandler.send_header("content-type", "application/json")
        requestHandler.end_headers()
        with open(r'.\signupmails.json', 'w') as f:
                            json.dump(json_object, f)
                            f.close()
        #curl -H "Content-Type: application/json" -d "{\"ok\":\"yes\"}" http://localhost:8000/signup
        requestHandler.wfile.write(bytes(json.dumps(json_object), "utf-8"))
        return