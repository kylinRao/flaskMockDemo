import asyncio
from lib.CONSTANTS import CONSTANTS
from time import sleep
import websockets
import json
async def report_log(log_content):
    async with websockets.connect(CONSTANTS.WEBSOCKET_URL) as websocket:
        res = {}
        res.update({"contentType": "reportLog"})
        res.update( {"content": log_content})
        await websocket.send(json.dumps(res))
        print({"contentType": "reportLog", "content": log_content})
if __name__ == '__main__':

    while 1:
        print("发送消息")

        asyncio.get_event_loop().run_until_complete(report_log("aaaaaaa"))
        sleep(5)
