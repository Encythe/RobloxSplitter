local RobloxSplitter = {}

local HTTP = game:GetService("HttpService")

local COMMAND_BASE = "[RobloxSplitter] "

function FireCommand(a0: {[string]: any})
	print(COMMAND_BASE .. HTTP:JSONEncode(a0))
end

-- Sets the splits on the timer.
-- If table length of splits is not exactly the length of available split slots, the command will either be undershoot or overshoot the splits.
function RobloxSplitter.SetSplits(Splits: {[number]: string})
	local command = {command = "SET_SPLITS", data = Splits}
	
	FireCommand(command)
end

-- Start the timer.
function RobloxSplitter.Start()
	local command = {command = "START"}
	
	FireCommand(command)
end

-- Split the currently active segment, or until the specified index.
-- Attempting to split to an already split segment will cause the command to be voided.
function RobloxSplitter.Split(split_until: number?)
	local command = {command = "SPLIT", data = split_until}
	
	FireCommand(command)
end

-- Split the currently active segment, or start the timer if it is not already running.
function RobloxSplitter.StartOrSplit(split_until: number?)
	local command = {command = "START_OR_SPLIT", data = split_until}
	
	FireCommand(command)
end

function RobloxSplitter.Reset()
	local command = {command = "RESET"}
	
	FireCommand(command)
end

return RobloxSplitter
