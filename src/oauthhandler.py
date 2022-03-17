import json
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.parse import urlencode
import http.client

class oAuthHandler:
    def __init__(self, *args, **kwargs):
        self.initOAuthCreds()

    def loadTemplate(self, component=None):
        if component is None:
            with open(r'.\oauth\template.html', 'r') as f:
                html_string = f.read()
            return html_string
        
        with open('.\oauth\{}.html'.format(component), 'r') as f:
            html_string = f.read()
        return html_string
        
    
    def initOAuthCreds(self):
        with open(r'.\refresh_token.json', mode='r') as f:
            data = json.load(f)
            #print(data)
            self.refresh_token = data["refresh_token"]
        self.gen_code = None
        with open(r'.\web_client_id.json', mode='r') as f:
            data = json.load(f)
            #print(data)
            self.client_id = data["web"]["client_id"]
            self.client_secret = data["web"]["client_secret"]
            self.auth_uri = data["web"]["auth_uri"]
            self.token_uri = data["web"]["token_uri"]
            self.redirect_uris = data["web"]["redirect_uris"]
            self.javascript_origins = data["web"]["javascript_origins"]

    def writeResponse(self, title, heading, content, requestHandler, component=None):
        if component is None:
                self.html_tpl = self.loadTemplate()
        else:
                self.html_tpl = self.loadTemplate(component)

        mapping = [(r"{title}",title),(r"{heading}", heading),(r"{content}", content)]

        for k,v in mapping:
            self.html_tpl = self.html_tpl.replace(k,v)

        requestHandler.wfile.write(bytes(self.html_tpl, "utf-8"))
    
    def handleOAuthAccessGET(self, requestHandler):       
        if requestHandler.url.query:
            query_params = parse_qs(requestHandler.url.query)
            if 'code' in query_params:
                #https://stackoverflow.com/questions/40557606/how-to-url-encode-in-python-3
                self.gen_code = query_params["code"][0] # first occurance/index due to otherwise inserting str chars ['variable_content']
            else:
                requestHandler.send_response(415, "Error: required parameter not found")
                requestHandler.end_headers()
                requestHandler.wfile.write(b"Error: required parameter not found")
                return
        else:
            requestHandler.send_response(415, "Error: no parameter")
            requestHandler.end_headers()
            requestHandler.wfile.write(b"Error: no parameter")
            return

        params = {'code': self.gen_code, 'client_id': self.client_id, 'client_secret': self.client_secret, 'redirect_uri': self.redirect_uris[0], 'grant_type': 'authorization_code'} 
        headers = {"content-type":"application/x-www-form-urlencoded"}
        #https://stackoverflow.com/questions/11763976/python-http-client-json-request-and-response-how
        conn = http.client.HTTPSConnection(urlparse(self.token_uri).netloc)
        #https://stackoverflow.com/questions/10588644/how-can-i-see-the-entire-http-request-thats-being-sent-by-my-python-application
        conn.request('POST', urlparse(self.token_uri).path, urlencode(params), headers)
        response = conn.getresponse()
        match response.status:
            case 200:
                #readlines instead of read, multiline response, json response returned as a list of bytes
                data = response.readlines()
                #https://stackoverflow.com/questions/30845669/convert-a-list-of-bytes-to-a-string-in-python-3?rq=1
                json_response = json.loads(bytes.join(b'', data).decode('ascii'))
                conn.close()
                json_object = json_response
                #https://stackoverflow.com/questions/23049767/parsing-http-response-in-python
                with open('access_token.json', 'w') as f:
                    json.dump(json_response, f)
                
                requestHandler.send_response(200)
                requestHandler.send_header("content-type", "text/html")
                requestHandler.end_headers()
                
                title = "Google Auth Success"
                heading = "Generated access token credentials"
                content = str(json_object) + "<ul><li><a href='/'>Back to default index document</a></li></ul>"

                self.writeResponse(title, heading, content, requestHandler)


            case _:
                print(response.status, response.reason, response.headers)
                requestHandler.send_response(400, "Bad Request")
                requestHandler.end_headers()

    def handleOAuthRedirectGET(self, requestHandler):
        if requestHandler.url.query:
            query_params = parse_qs(requestHandler.url.query)
            if 'code' and 'scope' in query_params:
                #https://stackoverflow.com/questions/40557606/how-to-url-encode-in-python-3
                self.gen_code = query_params["code"][0] # first occurance/index due to otherwise inserting str chars ['variable_content']
                requestHandler.send_response(200)
                requestHandler.send_header("content-type", "text/html")
                requestHandler.end_headers()

                title = "Google Auth Code Generation Success"
                heading = "Generated auth code to request an access token is"
                #https://www.kite.com/python/answers/how-to-insert-the-same-value-multiple-times-when-formatting-a-string-in-python
                content = self.loadTemplate("redirect_content").format(self.gen_code)

                self.writeResponse(title, heading, content, requestHandler)

            else:
                requestHandler.send_response(415, "Error: required parameter not found")
                requestHandler.end_headers()
                requestHandler.wfile.write(b"Error: required parameter not found")
        else:
            requestHandler.send_response(415, "Error: no parameter")
            requestHandler.end_headers()
            requestHandler.wfile.write(b"Error: no parameter")

    def handleOAuthRefreshGET(self, requestHandler):
        params = {'client_id': self.client_id, 'client_secret': self.client_secret, 'refresh_token': self.refresh_token, 'grant_type': 'refresh_token'} 
        headers = {"content-type":"application/x-www-form-urlencoded"}
        
        conn = http.client.HTTPSConnection(urlparse(self.token_uri).netloc)
        conn.request('POST', urlparse(self.token_uri).path, urlencode(params), headers)
        response = conn.getresponse()
        match response.status:
            case 200:
                #readlines instead of read, multiline response, json response returned as a list of bytes
                data = response.readlines()
                json_response = json.loads(bytes.join(b'', data).decode('ascii'))
                conn.close()
                json_object = json_response
                with open('access_token.json', 'w') as f:
                    json.dump(json_response, f)

                requestHandler.send_response(200)
                requestHandler.send_header("content-type", "text/html")
                requestHandler.end_headers()

                title = "Access Token Refreshed"
                heading = "Access token refreshed. New credentials"
                content = json.dumps(json_object) + "<ul><li><a href='/'>Back to default index document</a></li></ul>"

                self.writeResponse(title, heading, content, requestHandler)

            case _:
                print(response.status, response.reason, response.headers)
                requestHandler.send_response(400, "Bad Request")
                requestHandler.end_headers()