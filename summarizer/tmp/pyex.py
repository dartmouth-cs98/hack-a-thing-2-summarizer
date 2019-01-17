from aiohttp import web
import socketio
import json

sio = socketio.AsyncServer()

async def handler_wrapper(funcptr):
    

class pyex():
    def __init__(self):
        # Init server variables
        self.app = web.Application()
        sio.attach(self.app)

        self.register_function('connect', self.connect)
        self.register_function('disconnect', self.disconnect)

    # async def connect(self, sid):
    #     print("connected: ", sid)
    #     await sio.emit('connect', "connected")

    # async def disconnect(self, sid):
    #     print("disconnected: ", sid)
    #     await sio.emit('disconnect', "disconnected")

    # async def sendMessage(self, message):
    #     await sio.emit('summary_result', str(message))
    #     print("Emitted {}".format(message))
    #     return True

    # Method to register functions to the socket server.
    # Ex:   register_function("connect", connect_handler)
    def register_function(self, signal, funcptr):
        sio.on(signal)(funcptr)

    # Method that starts the socket server.
    # Must be called after registering functions
    def start(self):
        web.run_app(self.app)
# x = pyex()
# x.register_function('connect', connect)
# x.start()