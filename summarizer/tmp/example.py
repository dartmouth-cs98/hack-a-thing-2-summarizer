from pyex import pyex
import json

async def connect(sid, environ):
    print("Connected: " + str(sid))

def summarize_csv(sid, message):
    print("Received file: " + str(message))
    data = json.loads(message)
    print(data)


x = pyex()
x.register_function('connect', connect)
x.register_function('summarize_csv', summarize_csv)
x.start()