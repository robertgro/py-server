import os
import sys
import time
from subprocess import Popen
from src import requesthandler
from src import threadingmixin

if len(sys.argv) >= 2:
    HOST_NAME = sys.argv[1]
    PORT = int(sys.argv[2])
else:
    PORT = input("PORT (Default 8000) ")

    if not PORT:
        PORT = 8000

    HOST_NAME = input("HOST (Default 127.0.0.1) ")

    if not HOST_NAME:
        HOST_NAME = "127.0.0.1"

server = threadingmixin.ThreadedHTTPServer((HOST_NAME, PORT), requesthandler.myRequestHandler)

print(time.asctime(), 'Server UP - %s:%s' % (HOST_NAME, PORT))

Popen(f'{os.environ["ProgramFiles(x86)"]}/Google/Chrome/Application/chrome.exe http://{HOST_NAME}:{str(PORT)}')

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
    
print(time.asctime(), 'Server DOWN - %s:%s' % (HOST_NAME, PORT))
server.server_close()