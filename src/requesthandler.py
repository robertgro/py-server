import http.server
#import threading
from urllib.parse import urlparse
from src import ytdlhandler
from src import oauthhandler
from src import signuphandler

class myRequestHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.ytdl_handler = ytdlhandler.ytdlHandler()
        self.oauth_handler = oauthhandler.oAuthHandler()
        self.signup_handler = signuphandler.SignupHandler()
        super(myRequestHandler, self).__init__(*args, **kwargs)

    def do_POST(self):
        self.url = urlparse(self.path)
        match self.url.path:
            case "/signup":
                self.signup_handler.handleSignupPOST(self)

    def do_GET(self):
        #cur_thread = threading.currentThread()
        #print("cur_thread {}".format(cur_thread.name))
        self.url = urlparse(self.path)
        match self.url.path:
            case "/oauth":
                self.oauth_handler.handleOAuthRedirectGET(self)
            case "/oauth/access":
                self.oauth_handler.handleOAuthAccessGET(self)
            case "/oauth/refresh":
                self.oauth_handler.handleOAuthRefreshGET(self)
            case "/ytdl":
                self.ytdl_handler.handleIndex(self)
            case "/ytdl/dir":
                self.ytdl_handler.handleDirectoryGET(self)
            case "/ytdl/dl":
                self.ytdl_handler.handleDownloadGET(self)
            case "/ytdl/utils.js":
                filename = self.url.path[self.url.path.rfind("/") + 1:]
                self.ytdl_handler.serve_static(filename, self)
            case _:
                return http.server.SimpleHTTPRequestHandler.do_GET(self)

#https://stackoverflow.com/questions/35470510/python-attribute-error-type-object-has-no-attribute
        #before: self.handler = filename.handlername <- missing () for instance creation, was the class himself lol