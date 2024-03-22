import websocket
import json
import time
from uuid import uuid4
import threading

user_id = '097a021b-d2c6-4d01-a437-13847ff48b0e'
logger = print

device_id = str(uuid4())
logger("INFO: Device ID -", device_id)

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'

options = {
    'header': {
        'User-Agent': user_agent
    }
}

def on_message(ws, message):
    data = json.loads(message)
    if data['action'] == 'AUTH':
        auth_response = {
            'id': data['id'],
            'origin_action': 'AUTH',
            'result': {
                'browser_id': device_id,
                'user_id': user_id,
                'user_agent': options['header']['User-Agent'],
                'timestamp': int(time.time()),
                'device_type': 'extension',
                'version': '3.3.2'
            }
        }
        logger('RESPONSE: ', auth_response)
        ws.send(json.dumps(auth_response))
    elif data['action'] == 'PONG':
        pong_response = {'id': data['id'], 'origin_action': 'PONG'}
        logger('RESPONSE: ', pong_response)
        ws.send(json.dumps(pong_response))
    else:
        logger('RESPONSE: ', data)

def on_error(ws, error):
    logger('WebSocket error:', error)

def on_close(ws, *args):
    logger('WebSocket connection closed.')

    logger('Reconnecting...')
    time.sleep(180)
    ws.on_open = on_open
    ws.run_forever()

def on_open(ws):
    logger('WebSocket connection opened.')
    send_ping()

def send_ping():
    def run():
        while True:
            send_message = json.dumps({
                'id': device_id,
                'version': '1.0.0',
                'action': 'PING',
                'data': {}
            })
            logger('SENDING PING: ', send_message)
            ws.send(send_message)
            time.sleep(20)

    ping_thread = threading.Thread(target=run)
    ping_thread.daemon = True
    ping_thread.start()

if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("wss://proxy.wynd.network:4650/", header=options['header'], on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
