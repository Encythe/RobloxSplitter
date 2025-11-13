# RobloxSplitter
An open-source tool to automate splitting in Roblox games, functioning similarly to Bloxstrap's Discord Rich Presence.

### Disambiguation
This repository contains code for both the Client and the Library, to disambiguate between these two versions, you can refer to the table below:
| Variant | Description | Location |
| - | - | - |
| **RobloxSplitter Client** | This is the client hosted on the Speedrunner's machine used to communicate with LiveSplit.<br>It receives data from Roblox's Log files and parses it as commands. | [Source](https://github.com/Encythe/RobloxSplitter/blob/main/Source) |
| **RobloxSplitter Library** | This is the module for developers to incorporate autosplitting in their own games.<br>Commands are pre-defined in the module and can be called based on events in the game. | [Library](https://github.com/Encythe/RobloxSplitter/blob/main/Library) |

## DEMONSTRATIONS
https://github.com/user-attachments/assets/d74ccd60-6596-42a3-b65e-595a03ec7581

## Using the RobloxSplitter Client
To use the RobloxSplitter Client, you must first:

### Enable the LiveSplit Websocket
This can be done through the LiveSplit settings, or by following the following instructions:
1. Right Click on the LiveSplit modal.
2. Click on "Settings"
3. Under LiveSplit server, set **Startup Behavior** to "Start Websocket Server". Keep the port as is.
4. Save the changes, and restart LiveSplit. This should launch the WebSocket that RobloxSplitter can communicate with.

### Play in a supported game
Since this is still very early in production, no games have incorporated the **RobloxSplitter Library** into their gameplay yet.

Because of this, you must either test the **RobloxSplitter Client** in Studio, or by playing the test game, which can be found here: https://roblox.com/games/72499628119399

If you plan on playing the test game, you must have six splits in your current configuration, like the following:
<img width="555" height="222" alt="image" src="https://github.com/user-attachments/assets/366de387-d2e1-4d4e-a643-ebd0b6446f11" /><br>
This is because the test game itself has six splits, and also uses the very finnicky `RobloxSplitter.SetSplits()` Library function.

## Incorporating RobloxSplitter as a developer
To incorporate the RobloxSplitter Library into your game, simply place the [`RobloxSplitter.luau`](https://github.com/Encythe/RobloxSplitter/blob/main/Library/RobloxSplitter.luau) file or the [`RobloxSplitter Library Model`](https://create.roblox.com/store/asset/115654240793436) somewhere in `ReplicatedStorage`, after which you can require the module and call its various functions.

For code examples, see [`Example.luau`](https://github.com/Encythe/RobloxSplitter/blob/main/Library/Example.luau)
