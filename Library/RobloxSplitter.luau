local RobloxSplitter = {}

local RunService = game:GetService("RunService")
local HTTP = game:GetService("HttpService")

if not RunService:IsClient() then
	error("[RobloxSplitter] RobloxSplitter will not work in an environment other than the Client!")
end

local COMMAND_BASE = "[RobloxSplitter] "

-- Send the request to log file to be processed by the local server.
function FireCommand(a0: {[string]: any})
	print(COMMAND_BASE .. HTTP:JSONEncode(a0))
end

-- Sets the splits on the timer.
-- If table length of splits is not exactly the length of available split slots, the command will either be undershoot or overshoot the splits.
-- This is not recommended to be used due to the unpredictable nature of speedrunners' splits.
function RobloxSplitter.SetSplits(Splits: {[number]: string}): {[number]: string}
	local command = {command = "SET_SPLITS", data = Splits}

	FireCommand(command)
	return Splits
end

-- Start the timer.
function RobloxSplitter.Start()
	local command = {command = "START"}

	FireCommand(command)
end
RobloxSplitter.StartTimer = RobloxSplitter.Start

--[[
	!!! WARNING!
	!!! The <code>split_until</code> parameter is only really useful in single-category games!
	!!! If your game has more categories with a lot of room for mixing and matching, call <code>Split()</code> instead of <code>Split(number)</code>!

	Split the currently active segment, or until the specified index.
	Attempting to split to an already split segment using the split_until parameter will do nothing.
]]
function RobloxSplitter.Split(split_until: number?)
	local command = {command = "SPLIT", data = split_until}

	FireCommand(command)
end

--[[
	!!! WARNING!
	!!! The <code>split_until</code> parameter is only really useful in single-category games!
	!!! If your game has more categories with a lot of room for mixing and matching, call <code>Split()</code> instead of <code>Split(number)</code>!

	Split the currently active segment, or start the timer if it is not already running.
]]
function RobloxSplitter.StartOrSplit(split_until: number?)
	local command = {command = "START_OR_SPLIT", data = split_until}

	FireCommand(command)
end

-- Resets the timer.
function RobloxSplitter.Reset()
	local command = {command = "RESET"}

	FireCommand(command)
end

-- Pauses both the RTA [Real Time Attack] and IGT [In-Game Time] timer.
function RobloxSplitter.Pause()
	local command = {command = "PAUSE"}

	FireCommand(command)
end

-- Resumes/unpauses both the RTA [Real Time Attack] and IGT [In-Game Time] timer.
function RobloxSplitter.Resume()
	local command = {command = "RESUME"}

	FireCommand(command)
end
RobloxSplitter.Unpause = RobloxSplitter.Resume

-- Pauses the Game Timer. Allows RTA to continue counting up.
-- Usually used in the context of loading screens that have variable load times.
function RobloxSplitter.PauseGameTime()
	local command = {command = "PAUSE_GAME_TIME"}

	FireCommand(command)
end

-- Resumes/Unpauses the Game Timer.
-- Usually used in the context of loading screens that have variable load times.
function RobloxSplitter.ResumeGameTime()
	local command = {command = "RESUME_GAME_TIME"}

	FireCommand(command)
end
RobloxSplitter.UnpauseGameTime = RobloxSplitter.ResumeGameTime

-- Use IGT [In-Game Timer] as the primary timing method.
function RobloxSplitter.SwitchToGameTime()
	local command = {command = "SWITCH_TO_GAME_TIME"}

	FireCommand(command)
end
RobloxSplitter.UseIGT = RobloxSplitter.SwitchToGameTime

-- Use RTA [Real Time Attack] as the primary timing method.
function RobloxSplitter.SwitchToRealTime()
	local command = {command = "SWITCH_TO_REAL_TIME"}

	FireCommand(command)
end
RobloxSplitter.UseRTA = RobloxSplitter.SwitchToRealTime

-- Skips the currently active segment.
function RobloxSplitter.SkipSplit()
	local command = {command = "SKIP_SPLIT"}

	FireCommand(command)
end

-- Undoes the previous split.
function RobloxSplitter.UndoSplit()
	local command = {command = "UNDO_SPLIT"}

	FireCommand(command)
end
RobloxSplitter.Unsplit = RobloxSplitter.UndoSplit


return RobloxSplitter
