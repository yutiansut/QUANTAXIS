import websocket
import threading
import time
from websocket import create_connection

def on_message(ws, message):
    print (message)

def on_error(ws, error):
    print( error)

def on_close(ws):
    print ("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print ("thread terminating...")
    run()

if __name__ == "__main__":

    ws = websocket.WebSocketApp("ws://localhost:8000/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.send("login")
    print ("Sent")
    print ("Receiving...")
    result = ws.recv()
    print ("Received '%s'" % result)
    ws.on_open = on_open

    ws.close()
    ws.run_forever()
