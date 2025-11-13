import websockets
import asyncio
import os
import glob
import json
import threading
import time
import concurrent.futures
import traceback

from constants import * 

class LiveSplitSocket:
    def __init__(self, URL: str = "ws://localhost:16834/livesplit"):
        self.CONNECTED = False
        self.uri = URL
        
    async def __aenter__(self, *_): return self
    async def __aexit__(self, *_): pass
    
    async def connect(self):
        self.socket = await websockets.connect(self.uri)
        self.CONNECTED = True
        #woh

    async def send(self, arg: str):
        await self.socket.send(arg)
    
    async def get(self) -> str: 
        return await self.socket.recv()
    
    async def request(self, arg: str):
        await self.send(arg)
        return await self.get()
        
    async def parse_command(self, args: str | dict[str]):
        print(args)
        if not self.CONNECTED:
            print("[WARNING] The socket is not currently connected. Please call connect() before calling any commands.")
        
        if not isinstance(args, dict):
            try:
                JSON_COMMAND: dict[str] = json.loads(args)
            except json.JSONDecodeError:
                print("Invalid JSON payload received")
                return
        else:
            JSON_COMMAND = args
        
        COMMAND = JSON_COMMAND.get("command", None)
        DATA = JSON_COMMAND.get("data", None)
        
        if COMMAND is None: print(f"Invalid payload received"); return
        
        method = getattr(self, COMMAND, None)
        if method is None or not callable(method): print(f"Invalid command {COMMAND}"); return
        
        await method(DATA)
    
    """
        THE ACTUAL COMMANDS
    """
    # Sets the splits on the timer. Not recommended.
    async def SET_SPLITS(self, payload : list[str]):
        if isinstance(payload, list) is False:
            return # No
        
        for i,v in enumerate(payload):
            await self.send(SET_SPLIT_NAME(i, v))
            
    # Start the timer.
    async def START(self, _):
        await self.send(START_TIMER)
    
    # Split the currently active segment, or until the specified index.
    async def SPLIT(self, payload: int = None):
        if isinstance(payload, int):
            payload -= 1
            # Split until the index
            await int(self.request(GET_SPLIT_INDEX))
            
            if split_index == -1:
                # The timer isn't running.
                return
            
            if split_index > payload:
                # We're already at this split.
                return
            
            last_action = None
            last_index = -1
            while True:
                await self.send(GET_SPLIT_INDEX)
                split_index = int(await self.socket.recv())
                print(split_index, payload)

                if last_index == split_index and last_action == SKIP_SPLIT:
                    # We're likely already at the end so...
                    await self.send(SPLIT)
                    break
                last_index = split_index
                
                if split_index < payload: await self.send(SKIP_SPLIT); last_action = SKIP_SPLIT
                elif split_index <= payload: await self.send(SPLIT); break
                else: break
        else:
            await self.send(SPLIT)
    
    # Split the currently active segment, or start the timer if it is not already running.
    async def START_OR_SPLIT(self, payload: int = None):
        await self.send(GET_SPLIT_INDEX)
        split_index = int(await self.socket.recv())
        
        if split_index == -1:
            await self.send(START_TIMER)
            if isinstance(payload, int) is False: return
        elif isinstance(payload, int) is False:
            await self.send(SPLIT)
            return
            
        await self.SPLIT(payload)
        
    # Resets the timer.
    async def RESET(self, _):
        await self.send(RESET)
        
    # Pauses the timer. Do not use this in an IGT [In-Game Timer] context.
    async def PAUSE(self, _):
        await self.send(PAUSE)
    
    # Resumes/unpauses the timer. Do not use this in an IGT [In-Game Timer] context.
    async def RESUME(self, _):
        await self.send(RESUME)

    # Pauses the Game Timer. Allows RTA to continue counting up.
    async def PAUSE_GAME_TIME(self, _):
        await self.send(PAUSE_GAME_TIME)
    
    # Resumes/Unpauses the Game Timer.
    async def RESUME_GAME_TIME(self, _):
        await self.send(UNPAUSE_GAME_TIME)
        
    # Use IGT [In-Game Timer] as the primary timing method.
    async def SWITCH_TO_GAME_TIME(self, _):
        await self.send(SWITCH_TO_GAMETIME)

    # Use RTA [Real Time Attack] as the primary timing method. 
    async def SWITCH_TO_REAL_TIME(self, _):
        await self.send(SWITCH_TO_REALTIME)
    
    # Skips the currently active segment.
    async def SKIP_SPLIT(self, _):
        await self.send(SKIP_SPLIT)

    # Undoes the previous split.
    async def UNDO_SPLIT(self, _):
        await self.send(UNSPLIT)

async def track_log_file(socket: LiveSplitSocket, path: str):
    print(f"Monitoring file: {path}")
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
                    await asyncio.sleep(.05)
                    continue

            line = file.readline()

            if not line:
                await asyncio.sleep(.01)
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
                print("\n" + line.rstrip("\n"))
                command = line.split("[RobloxSplitter] ", 1)[1].rstrip("\n")
                try:
                    await socket.parse_command(command)
                except BaseException as e:
                    print(f"[ERROR] {command} failed to parse.\n{e}")
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
        print("Connecting to LiveSplit...")
        try:
            await socket.connect()
            print("Connected to LiveSplit")
        except ConnectionRefusedError:
            print("[CRITICAL] RobloxSplitter failed to connect to the LiveSplit Websocket.\nEither the LiveSplit server is not running, or something else is preventing RobloxSplitter from connecting.")
            os.system("pause")
            return

        logs_dir = os.path.join(os.getenv("LOCALAPPDATA", ""), "Roblox", "Logs")
        if not os.path.exists(logs_dir):
            print("[CRITICAL] Could not locate Roblox logs directory, which is crucial for RobloxSplitter to function properly.")
            os.system("pause")
            return
            
        watcher = asyncio.create_task(watch_logs(socket, logs_dir))

        try:
            async def _close_socket(socket: LiveSplitSocket):
                socket.CONNECTED = False
                
                try:
                    if getattr(socket, "socket", None) is not None:
                        await socket.socket.close()
                except Exception:
                    pass

            async def _poller_thread_fn(socket: LiveSplitSocket):
                backoff = 0.5
                while True:
                    try:
                        message = await socket.request(PING)
                        if message != "pong":
                            raise Exception("The websocket did not receive a valid ping response.")
                        
                        backoff = 0.5
                    except concurrent.futures.CancelledError:
                        return
                    except Exception as e:
                        # print it once please
                        if socket.CONNECTED == True:
                            print(e)
                            print('LiveSplit pipe disconnected, trying to reconnect in a moment...')

                        try:
                            await _close_socket(socket)
                        except Exception:
                            pass

                        while True:
                            try:
                                await asyncio.sleep(backoff)
                                print("Reconnecting to LiveSplit...")
                                await socket.connect()
                                print("Reconnected to LiveSplit")
                                break
                            except Exception as e2:
                                print(f"Reconnect failed: {e2} // Retrying in {backoff} seconds...")
                                backoff = min(backoff + 0.5, 10.0)
                                continue

                    await asyncio.sleep(1)

            poller_task = asyncio.create_task(_poller_thread_fn(socket))
            await poller_task # this just works??? okay.
            await watcher
        except asyncio.CancelledError:
            watcher.cancel()
            raise

if __name__ == "__main__":
    asyncio.run(main())