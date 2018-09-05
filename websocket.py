from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from flask import request,abort,Flask,jsonify
import base64
import threading
import cv2
clients = []
app = Flask(__name__)

class SimpleEcho(WebSocket):

    def handleMessage(self):
        # echo message back to client
        #encoded_string = self.readb64(self.data)
        #self.sendMessage(self.data)
        #print(len(clients))
        name = self.data[0:6]
        image = self.data[6:]

        for client in clients:
            #print(unicode("data:image/png;base64,"+self.data, "utf-8"))
            client.sendMessage(u''+name)
            client.sendMessage(u'data:image/png;base64,'+image)

    def handleConnected(self):
        print(self.address, 'connected')
        clients.append(self)
        for client in clients:
            with open("tester.png", "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                client.sendMessage(unicode("data:image/png;base64,"+encoded_string, "utf-8"))
            
            #print(encoded_string)

    def handleClose(self):
        clients.remove(self)
        print(self.address, 'closed')
        
@app.route('/unlock',methods = ['POST'])
def unlock():
    if not request.json or not 'passcode' in request.json: 
        abort(401)
    else:
        #replace here with database code
        passcode = request.json['passcode']
        username = request.json['user']
        
        if passcode == "pass1" and username =="Edward":
            print("Executing command to unlock")
            return 'successful authentication'
        elif passcode == "pass2" and username =="ruth":
            print("Executing command to unlock")
            return 'successful authentication'
        else:
            return 'error!'
        
if __name__ == '__main__':
    thread = []
    server = SimpleWebSocketServer('', 8000, SimpleEcho)
    print("Getting websocket thread ready")
    app.use_reloader=False
    app.debug = False
    t = threading.Thread(target=server.serveforever)
    print("Now running flask")
    t.daemon = True
    t.start()
    tx = threading.Thread(target=app.run(host='0.0.0.0',port=8080))
    tx.start()

    # app.run(debug=True,host='0.0.0.0',port=8080)

