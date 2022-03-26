const filename_pattern = /\.mp4|\.m4a/;
const fin_pattern = /[0-9]{1,3}% of [0-9]{1,}.[0-9]{1,}KiB in [0-9]{2}:[0-9]{2}/;
const prog_pattern = /[0-9]{1,}\.[0-9]% of [0-9]{1,}\.[0-9]{1,}(KiB|MiB|GiB) at\s+[0-9]{1,}\.[0-9]{2}(KiB|MiB|GiB)\/s ETA [0-9]{2}:[0-9]{2}/;

class myWebSocket {
    static async getWebSocket() {
        try {
            const server = await this.connectWebsocket();
            //console.log(server, "initialized");
            return server;
        } catch (error) {
            console.log("ooops ", error);
            // https://stackoverflow.com/questions/2381572/how-can-i-trigger-a-javascript-event-click
            document.getElementById("downloadButton").click();
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

            const return_filename = (output_str, ext_str) => {
                let i = output_str.lastIndexOf("\\") + 1;
                let ext = output_str.lastIndexOf(ext_str) + 4;
                return output_str.substring(i,ext)
            }

            var ext = ".mp4";
        
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
                //console.log("From Server: " + e.data, "Type: " + typeof(e.data));

                // https://stackoverflow.com/questions/762011/whats-the-difference-between-using-let-and-var
                // https://stackoverflow.com/questions/8826385/how-to-search-the-children-of-a-htmldivelement
                var res = document.getElementById("result").getElementsByTagName("small")[0];

                //https://stackoverflow.com/questions/2896626/switch-statement-for-string-matching-in-javascript
                switch(true) {
                    case /100% of .* in/.test(e.data):
                        res.style.color = "green";
                        res.innerText = "Erledigt.";
                        break;
                    case /Deleting/.test(e.data):
                        break;
                    case filename_pattern.test(e.data):
                        ext = filename_pattern.exec(e.data)[0];
                        document.getElementById("cat").innerText = return_filename(e.data, ext);
                        break;
                    case /has already been downloaded and merged/.test(e.data):
                        res.innerText = "Das Video " + return_filename(e.data, ext) + " existiert bereits.";
                        break;
                    case prog_pattern.test(e.data):
                        res.style.color = "black";
                        res.innerText = prog_pattern.exec(e.data)[0];
                        break;
                    case fin_pattern.test(e.data):
                        res.style.color = "black";
                        res.innerText = fin_pattern.exec(e.data)[0];
                        break;
                    default:
                        //console.log("DEBUG", e.data);
                        break;
                }

                /*
                For blob messages

                if (e.data instanceof Blob) {
                    const reader = new FileReader();
                    reader.onload = () => {
                        const result = document.getElementById("result");
                        const pattern = /[0-9]{1,3}% of [0-9]{1,}.[0-9]{1,}KiB in [0-9]{2}:[0-9]{2}/;
                        console.log("Incoming Data:", reader.result);
                    }
                    reader.readAsText(e.data);
                    }
                    */
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
    setTimeout(()=>{},300);
    myWebSocket.getWebSocket().catch((error) => {
        console.error(error);
    });
}