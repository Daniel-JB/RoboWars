from websockets import serve
import asyncio
import json

class Server():
    players = {}

    async def echo(self, websocket):
        async for message in websocket:
            data = json.loads(message)
            print("Message: " + str(data))
            print(str(data['name']))
            await websocket.send(message)

    async def createRoom(self):
        async with serve(self.echo, "localhost", 8765):
            await asyncio.Future()  # run forever




asyncio.run(Server().createRoom())
