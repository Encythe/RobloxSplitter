import websockets
import asyncio
import keyboard
import os
import glob
import json

from constants import * 

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
            print("[WARNING] The socket is not currently connected. Please call connect() before calling any commands.")
        print(args)
        if not isinstance(args, dict):
            JSON_COMMAND: dict[str] = json.loads(args)
        
        COMMAND = JSON_COMMAND.get("command", None)
        DATA = JSON_COMMAND.get("data", None)
        
        if COMMAND is None: print(f"Invalid payload received"); return
        if self.callbacks.get(COMMAND, None) is None: print(f"Invalid command {COMMAND}"); return
        
        await self.callbacks.get(COMMAND)(DATA)
    
    # Sets the splits on the timer. Not recommended.
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
            
            if split_index > payload:
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
    
    # Split the currently active segment, or start the timer if it is not already running.
    async def START_OR_SPLIT(self, payload: int = None):
        await self.socket.send(GET_SPLIT_INDEX)
        split_index = int(await self.socket.recv())
        
        if split_index == -1:
            await self.socket.send(START_TIMER)
            if isinstance(payload, int) is False: return
        elif isinstance(payload, int) is False:
            await self.socket.send(SPLIT)
            return
            
        await self.SPLIT(payload)
        
    # Reset the timer.
    async def RESET(self, _):
        await self.socket.send(RESET)

async def track_log_file(socket: LiveSplitSocket, path: str):
    print(f"Tracking file: {path}")
    file = None
    inode = None
    try:
        while True:
            if file is None:
                try:
                    file = open(path, "r", encoding="utf-8", errors="ignore")
                    file.seek(0, os.SEEK_END)
                    try:
                        inode = os.stat(path).st_ino
                    except Exception:
                        inode = None
                except FileNotFoundError:
                    await asyncio.sleep(0.5)
                    continue

            line = file.readline()
            if not line:
                await asyncio.sleep(0.1)
                try:
                    st = os.stat(path)
                    if inode is None or getattr(st, "st_ino", None) != inode:
                        try:
                            file.close()
                        except Exception:
                            pass
                        file = open(path, "r", encoding="utf-8", errors="ignore")
                        inode = getattr(st, "st_ino", None)
                        file.seek(0, os.SEEK_END)
                except FileNotFoundError:
                    try:
                        file.close()
                    except Exception:
                        pass
                    file = None
                    inode = None
                continue

            if "[FLog::Output] [RobloxSplitter] " in line:
                command = line.split("[RobloxSplitter] ", 1)[1].rstrip("\n")
                await socket.parse_command(command)
    except asyncio.CancelledError:
        # clean up
        try:
            if file:
                file.close()
        except Exception:
            pass
        raise
    except Exception as e:
        print(f"Error tracking {path}: {e}")
        try:
            if file:
                file.close()
        except Exception:
            pass

async def watch_logs(socket: LiveSplitSocket, logs_dir: str):
    tasks: dict[str, asyncio.Task] = {}
    while True:
        try:
            found = set(glob.glob(os.path.join(logs_dir, "*.log")))
        except Exception:
            found = set()

        for file in found:
            if file not in tasks:
                tasks[file] = asyncio.create_task(track_log_file(socket, file))

        for file in list(tasks.keys()):
            if file not in found:
                t = tasks.pop(file)
                t.cancel()

        await asyncio.sleep(1.0)

async def main():
    async with LiveSplitSocket() as socket:
        await socket.connect()

        logs_dir = os.path.join(os.getenv("LOCALAPPDATA", ""), "Roblox", "Logs")
        if not os.path.exists(logs_dir):
            print("[CRITICAL] Could not locate Roblox logs directory, which is crucial for the program to function properly.\nPress any key to exit the program...")
            os.system("pause")
            return
            
        watcher = asyncio.create_task(watch_logs(socket, logs_dir))

        try:
            await watcher
        except asyncio.CancelledError:
            watcher.cancel()
            raise

if __name__ == "__main__":
    asyncio.run(main())