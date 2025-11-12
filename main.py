import websockets
import asyncio
import keyboard
import os
import glob
import json

from constants import * 

random_splits = [
    "that one",
    "unby6",
    "horse incarnate",
    "jesu the spider is here",
    "h",
    "what am i typing"
]

class LiveSplitSocket:
    def __init__(self, URL: str = "ws://localhost:16834/livesplit"):
        self.CONNECTED = False
        self.uri = URL
        
        self.callbacks = {
            "SET_SPLITS": self.SET_SPLITS,
            "START": self.START,
            "SPLIT": self.SPLIT,
            "RESET": self.RESET,
            "START_OR_SPLIT": self.START_OR_SPLIT
        }
        
    async def __aenter__(self, *_): return self
    async def __aexit__(self, *_): pass
    
    async def connect(self):
        self.socket = await websockets.connect(self.uri)
        self.CONNECTED = True
        print("Connected to LiveSplit")
        #woh
        
    async def parse_command(self, args: str):
        if not self.CONNECTED:
            print("[WARNING] The socket is not currently connected. Please call .connect() before calling any commands.")
        print(args)
        if not isinstance(args, dict):
            JSON_COMMAND: dict[str] = json.loads(args)
        
        COMMAND = JSON_COMMAND.get("command", None)
        DATA = JSON_COMMAND.get("data", None)
        
        if COMMAND is None: print(f"Invalid payload received"); return
        if self.callbacks.get(COMMAND, None) is None: print(f"Invalid command {COMMAND}"); return
        
        await self.callbacks.get(COMMAND)(DATA)
    
    # Sets the splits on the timer.
    async def SET_SPLITS(self, payload : list[str]):
        for i,v in enumerate(payload):
            await self.socket.send(SET_SPLIT_NAME(i, v))
            
    # Start the timer.
    async def START(self, _):
        await self.socket.send(START_TIMER)
    
    # Split the currently active segment, or until the specified index.
    async def SPLIT(self, payload: int = None):
        if isinstance(payload, int):
            payload -= 1
            # Split until the index
            await self.socket.send(GET_SPLIT_INDEX)
            split_index = int(await self.socket.recv())
            
            if split_index == -1:
                # The timer isn't running.
                return
            
            if split_index >= payload:
                # We're already at this split.
                return
            
            while True:
                await self.socket.send(GET_SPLIT_INDEX)
                split_index = int(await self.socket.recv())
                
                if split_index < payload: await self.socket.send(SKIP_SPLIT)
                elif split_index <= payload: await self.socket.send(SPLIT) 
                else: break
        else:
            await self.socket.send(SPLIT)
    
    async def START_OR_SPLIT(self, payload: int = None):
        await self.socket.send(GET_SPLIT_INDEX)
        split_index = int(await self.socket.recv())
        
        if split_index == -1:
            await self.socket.send(START_TIMER)
            if isinstance(payload, int) is False: return
        elif isinstance(payload, int) is False:
            await self.socket.send(SPLIT)
            return
            
            
        
        payload -= 1
        
        await self.socket.send(GET_SPLIT_INDEX)
        split_index = int(await self.socket.recv())
        
        if split_index == -1:
            # The timer isn't running.
            return
        
        if split_index > payload:
            # We're already at this split.
            return
        
        while True:
            await self.socket.send(GET_SPLIT_INDEX)
            split_index = int(await self.socket.recv())
            
            if split_index < payload: await self.socket.send(SKIP_SPLIT)
            elif split_index <= payload: await self.socket.send(SPLIT) 
            else: break
    
    async def RESET(self, _):
        await self.socket.send(RESET)
        

async def main():
    async with LiveSplitSocket() as socket:
        await socket.connect()
        
        list_of_files = glob.glob(os.getenv("LOCALAPPDATA") + r"\Roblox\Logs\*.log") 
        latest_file = max(list_of_files, key=os.path.getctime)
        
        file = open(latest_file)
        file.seek(0, os.SEEK_END)
        
        print(file)
        
        while True:
            line = file.readline()
            
            if not line:
                await asyncio.sleep(.1)
                continue
            
            if line.find("[FLog::Output] [RobloxSplitter] ") != -1:
                print(line)
                command = line.split("[RobloxSplitter] ")[1]
                await socket.parse_command(command)
                
            line.rstrip('\n')
            
            

        
            
if __name__ == "__main__":
    asyncio.run(main())


