import asyncio
from websockets import connect
import json 


async def sendCreateRobot(uri, name, base64):
    dictionary = {
        "name": name,
        "image": base64
    }
    async with connect(uri) as websocket:
        await websocket.send(json.dumps(dictionary, indent = 4) )
        
async def senUpdateRobot(uri, name, base64):
    dictionary = {
        "name": name,
        "commands": [
            {"turnLeft"},
            {"turnRight"},
            {"shoot"}
        ]
    }
    
    async with connect(uri) as websocket:
        await websocket.send(json.dumps(dictionary, indent = 4) )
        

asyncio.run(sendCreateRobot("ws://localhost:8765", "Daniel" , ""))