class myWebSocket {
    static async getWebSocket() {
        try {
            const server = await this.connectWebsocket();
            //console.log(server, "initialized");
            return server;
        } catch (error) {
            //console.log("ooops ", error);
            return error;
        }
    }

    static async connectWebsocket() {
        if (this.connectWebsocket.server && this.connectWebsocket.server.readyState < 2) {
            //console.log("reusing the socket connection [state = " + this.connectWebsocket.server.readyState + "]: " + this.connectWebsocket.server.url);
            return Promise.resolve(this.connectWebsocket.server);
          }
        
          return new Promise(function (resolve, reject) {
        
            const server = new WebSocket("ws://localhost:8765");
        
            server.onopen = function () {
              //console.log("socket connection is opened [state = " + server.readyState + "]: " + server.url);
              resolve(server);
            };
        
            server.onerror = function (err) {
              //console.error("socket connection error : ", err);
              reject(err);
            };

            server.onclose = function (e) {
                //console.log("onclose wsreadystate", ws.readyState);
                //console.log("Websocket Close", e.wasClean, e.code, e.reason);
                //console.log("Disconnected"); // task fulfilled
            };

            server.onmessage = function (e) {
                //console.log("From Server: " + e.data);
                if (e.data instanceof Blob) {
                    const reader = new FileReader();
                    reader.onload = () => {
                        const result = document.getElementById("result");
                        const pattern = /[0-9]{1,3}% of [0-9]{1,}.[0-9]{1,}KiB in [0-9]{2}:[0-9]{2}/;
                        //console.log("Incoming Data:", reader.result);
                        if (/has already been downloaded and merged/.test(reader.result)) {
                            let b = reader.result.lastIndexOf("\\") + 1;
                            let e = reader.result.lastIndexOf(".mp4") + 4;
                            result.innerText = "Das Video " + reader.result.substring(b,e) + " existiert bereits.";
                        } else if (pattern.test(reader.result)) {
                            result.innerText = pattern.exec(reader.result);
                        }
                    }
                    reader.readAsText(e.data);
                    }
            };

        // https://stackoverflow.com/questions/18803971/websocket-onerror-how-to-read-error-description
        // https://stackoverflow.com/questions/15705948/python-socketserver-timeout
        // https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code

          });
    }
}

function getDir(event) {
    event.preventDefault();
    fetch('/ytdl/dir')
    .then(response => response.text())
    .then(data => document.getElementById("dir").innerText = data);
    // https://stackoverflow.com/questions/19030742/difference-between-innertext-innerhtml-and-value
}

function initDownload(event) {
    const link = document.getElementById("link").value;
    const format = document.getElementById("format").value;
    event.preventDefault();
    if (!link) {
        alert("Bitte einen Link eingeben");
        return;
    }
    let url = '/ytdl/dl?link=' + encodeURIComponent(link) + "&format=" + format;
    fetch(url).catch((error) => console.log('Error:', error));
    myWebSocket.getWebSocket().then(function(server) { 
        //console.log(server.url, "is ready"); 
    }).catch((error) => {
        console.error(error);
    });
}