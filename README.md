# RobloxSplitter
An open-source tool to automate splitting in Roblox games, functioning similarly to Bloxstrap's Discord Rich Presence.

## DEMONSTRATIONS
https://github.com/user-attachments/assets/d74ccd60-6596-42a3-b65e-595a03ec7581

## Using RobloxSplitter
To use RobloxSplitter, you must first:

### Enable the LiveSplit Websocket
This can be done through the LiveSplit settings, or by following the following instructions:
1. Right Click on the LiveSplit modal.
2. Click on "Settings"
3. Under LiveSplit server, set **Startup Behavior** to "Start Websocket Server". Keep the port as is.
4. Save the changes, and restart LiveSplit. This should launch the WebSocket that RobloxSplitter can communicate with.

### Play in a supported game
Since this is still very early in production, no games have incorporated the RobloxSplitter library into their gameplay yet.

Because of this, you must either test RobloxSplitter in Studio, or by playing the test game, which can be found here: https://roblox.com/games/72499628119399

If you plan on playing the test game, you must have six splits in your current configuration, like the following:
<img width="555" height="222" alt="image" src="https://github.com/user-attachments/assets/366de387-d2e1-4d4e-a643-ebd0b6446f11" /><br>
This is because the test game itself has six splits, and also uses the very finnicky `RobloxSplitter.SetSplits()` library function.
