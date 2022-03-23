# py-server

expanding the http.server.SimpleHTTPRequestHandler python module to provide several helpful local listener interfaces for
- retrieving an google auth token and code for internal app usage (file upload automation)
- wrapping up youtube-dl.exe on windows, providing a simple ui including a websocket client (js) <> server (python) connection (streaming download progress), utilizing ms ps exec app to grab users desired download dir in an interactive windows user session mode
- signup cred generation to simplify a signup process

# install on win10

download and run install_py-server.cmd. it will create a new project directory (* also git init and python venv) and clones the origin master repo into it. pip_install_dep.cmd cares for pip requirement.txt install in the current venv.

to test the google oauth and signupmail service/route (if you really want to do this) you'll need to generate and download your own json files. replace the href in index.html with the google auth url to get it working. 

# prerequisite for youtube-dl

download youtube-dl.exe, ffmpeg.exe and generate youtube.com cookies via Get cookies chrome extension. place these files in an arbitrary location and correct the paths in src/ytdlhandler.py.

download sysinternals psexec.exe and place it in "C:\sysinternals\" or an arbitrary dir and correct the Popen arg 0 in src/ytdlhandler.py with the appropriate path.

this project is a work in progress. additional services and features will be added over time.
