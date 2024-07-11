import websockets
import asyncio

import time

async def start_websocket():
    async with websockets.connect("ws://backend-rest:8068") as websocket:
        async for message in websocket:
            print(message)

if __name__ == "__main__":
    time.sleep(10)
    asyncio.run(start_websocket())
