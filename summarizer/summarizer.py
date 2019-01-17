from aiohttp import web
import socketio
from summarize import GTSummarizer
import json

# Set up socket server
sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

# Init summarizer
summarizer = GTSummarizer()

# Socket events
@sio.on('connect')
async def connect(sid, environ):
    print("connected: ", sid)
    await sio.emit('connect', "connected")

# Summarize a csv path
@sio.on('summarize_csv')
async def summarize_csv(sid, data):

    # Call summarizer
    summary_results = summarizer.summarize_csv_wrapper(sid, data)
    
    # Build results
    result_obj = {}
    result_obj['result'] = summary_results
    result_str = json.dumps(result_obj)

    # Send results to client
    await sio.emit('summary_result', result_str)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

web.run_app(app)