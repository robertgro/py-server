import asyncio
from msilib.schema import Error
import signal
import subprocess
import threading
from unicodedata import east_asian_width
from urllib.parse import parse_qs
import re
import websockets
import time
import os

class ytdlHandler:
    def __init__(self, *args, **kwargs):
        self.loadLastPath()
        self.bin_path = r"C:\bin\youtube-dl.exe"
        self.cookie_path = r".\youtube-dl\youtube.com_cookies.txt"
        self.ffmpeg_path = r"C:\bin\ffmpeg.exe"

    def serve_static(self, filename, requestHandler):
        filepath = r'.\youtube-dl\{}'.format(filename)
        last_modified = str(time.strftime('%a, %d %b %Y %X GMT', time.gmtime(os.path.getmtime(filepath))))
        file = open(filepath, 'r').read()
        #https://stackoverflow.com/questions/7983820/get-the-last-4-characters-of-a-string
        match filename[-3:]:
            case ".js":
                requestHandler.send_response(200)
                requestHandler.send_header("content-type", "text/javascript")
                requestHandler.send_header("content-length", str(len(file)))
                requestHandler.send_header("last-modified", last_modified)
                requestHandler.end_headers()
                requestHandler.wfile.write(bytes(file, "utf-8"))
                return
            case _:
                print(filename)
                requestHandler.send_response(400, "Bad Request")
                requestHandler.end_headers()

    def loadLastPath(self):
        with open(".\includes\last_dir.path", 'r') as f:
            self.last_path = f.read()

    def loadTemplate(self, component=None):
        #https://stackoverflow.com/questions/51794609/how-to-import-html-file-into-python-variable
        if component is None:
            with open(r'.\youtube-dl\template.html', 'r') as f:
                html_string = f.read()
            return html_string
        
        with open('.\youtube-dl\{}.html'.format(component), 'r') as f:
            html_string = f.read()
        return html_string

    def writeResponse(self, title, heading, content, requestHandler, component=None):
        if component is None:
                self.html_tpl = self.loadTemplate()
        else:
                self.html_tpl = self.loadTemplate(component)

        mapping = [(r"{title}",title),(r"{heading}", heading),(r"{content}", content)]

        for k,v in mapping:
            self.html_tpl = self.html_tpl.replace(k,v)

        requestHandler.wfile.write(bytes(self.html_tpl, "utf-8"))

    def handleDownloadGET(self, requestHandler):
        if requestHandler.url.query:
            query_params = parse_qs(requestHandler.url.query)
            if 'link' and 'format' in query_params:
                self.link = query_params["link"][0]
                if not re.search("youtube.com", self.link):
                    requestHandler.send_response(415, "Error: unsupported media (malformed link)")
                    requestHandler.end_headers()
                    requestHandler.wfile.write(b"Error: unsupported media (malformed link)")
                self.dl_format = query_params["format"][0]
                self.loadLastPath()
                self.last_path = self.last_path[:-1]
                self.last_path += "/%(title)s.%(ext)s"
                #cmd = [self.bin_path, "--rm-cache-dir"]
                #subprocess.run(cmd, capture_output=True)
                match self.dl_format:
                    case "both":
                        cmd = [self.bin_path, "--cookies", self.cookie_path, "-f", "bestvideo[ext!=webm]+bestaudio[ext!=webm]/best[ext!=webm]", "--ffmpeg-location", self.ffmpeg_path, "-o", self.last_path, self.link]
                    case "audio":
                        cmd = [self.bin_path, "--cookies", self.cookie_path, "-f", "140/bestaudio[ext!=webm]", "--ffmpeg-location", self.ffmpeg_path, "-o", self.last_path, self.link]
                    case "video":
                        cmd = [self.bin_path, "--cookies", self.cookie_path, "-f", "137/bestvideo[ext!=webm]/best[ext!=webm]", "--ffmpeg-location", self.ffmpeg_path, "-o", self.last_path, self.link]
                    case _:
                        print("Error: self.link {}".format(self.dl_format))
                        requestHandler.send_response(400, "Bad Request")
                        requestHandler.end_headers()
                
                threading.Thread(target=wsProgressHandler('localhost', 8765, cmd).serve_forever).start()
                
                requestHandler.send_response(301)
                requestHandler.send_header("Location", "/ytdl")
                requestHandler.end_headers()

            else:
                requestHandler.send_response(415, "Error: required parameter not found")
                requestHandler.end_headers()
                requestHandler.wfile.write(b"Error: required parameter not found")
        else:
            requestHandler.send_response(415, "Error: no parameter")
            requestHandler.end_headers()
            requestHandler.wfile.write(b"Error: no parameter")
    
    def handleIndex(self, requestHandler):

        if self.last_path is None:
            self.loadLastPath()

        requestHandler.send_response(200)
        requestHandler.send_header("content-type", "text/html")
        requestHandler.end_headers()

        title = "youtube-dl.exe wrapper"
        heading = "youtube-dl.exe wrapper"
        content = self.loadTemplate("main_form")

        content = content.replace("{lastpath}", self.last_path)

        self.writeResponse(title, heading, content, requestHandler)

    def handleDirectoryGET(self, requestHandler):
        proc = subprocess.Popen(["C:\sysinternals\psexec.exe", "-nobanner", "powershell", "-NoLogo", "-ExecutionPolicy", "Unrestricted", "-File", ".\includes\get_dir.ps1"], stderr=subprocess.PIPE)

        while proc.returncode is None:
            try:
                proc.wait(10) # every 10 sec
            except subprocess.TimeoutExpired:
                pass

        proc.stderr.flush() #suppress psexec exit code msg

        self.loadLastPath()

        requestHandler.send_response(200)
        requestHandler.send_header("content-type", "text/plain")
        requestHandler.send_header("content-length", str(len(self.last_path)))
        requestHandler.send_header("connection", "keep-alive")
        requestHandler.send_header("keep-alive", "timeout=10, max=30")
        requestHandler.end_headers()
        requestHandler.wfile.write(bytes(self.last_path, "utf-8"))

class wsProgressHandler:
    
    server = None

    def __init__(self, host, port, cmd) -> None:
        self.host = host
        self.port = port
        self.cmd = cmd
        pass

    # https://github.com/python/cpython/blob/3.10/Lib/http/server.py

    monthname = [None,
                 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    def log_date_time_string(self):
        """Return the current time formatted for logging."""
        now = time.time()
        year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
        s = "%02d/%3s/%04d %02d:%02d:%02d" % (
                day, self.monthname[month], year, hh, mm, ss)
        return s

    def serve_forever(self):
        return asyncio.run(self.serve())

    async def serve(self):
        # on windows we need to enable reuse_address to prevent OSError sock in use
        #https://docs.python.org/3/library/asyncio-stream.html see start_server  params
        async with websockets.serve(self.handle, self.host, self.port, reuse_address=True):
            await asyncio.Future()


    async def handle(self, websocket):
        with subprocess.Popen(self.cmd, stdout=subprocess.PIPE) as proc:
            while proc.returncode is None:
                try:
                    line = proc.stdout.readline()
                    #print(line)
                    # todo regex split str(line) by \r to stream download progress
                    proc.stdout.flush()
                    if not line:
                        break
                    await websocket.send(line)
                    await asyncio.sleep(0.5)
                except Exception as e:
                    print("Error", e)
        print('{}:{} - - [{}] "DEBUG sock handled {}."'.format(self.host, self.port, self.log_date_time_string(), self.cmd[len(self.cmd) - 1]))