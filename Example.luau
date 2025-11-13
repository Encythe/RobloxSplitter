local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")
local UIS = game:GetService("UserInputService")

local LocalPlayer = Players.LocalPlayer

local RobloxSplitter = require(ReplicatedStorage.RobloxSplitter)

while true do
	RobloxSplitter.Reset()
	RobloxSplitter.UseIGT()
	RobloxSplitter.SetSplits({
		"Press W",
		"Press A",
		"Press S",
		"Press D",
		`Send "Nice!"`,
		"Jump"
	}) -- Needs 6 free slots
	
	local Character = LocalPlayer.Character or LocalPlayer.CharacterAdded:Wait()
	
	task.wait(2)
	
	for i = 3, 1, -1 do
		print(i..`...`)
		script:FindFirstChild(`c{i}`):Play()
		task.wait(1)
	end

	print("GO!")
	local GameTime = os.clock()
	RobloxSplitter.Start()
	
	local HighestSplit = 0
	local CanReset = false
	
	local function SplitIncrement()
		RobloxSplitter.Split()
		HighestSplit += 1
	end
	
	local References = {
		[0] = "W",
		[1] = "A",
		[2] = "S",
		[3] = "D",
		-- No
		[5] = "Space",
	}
	
	local Connection1 = UIS.InputBegan:Connect(function(input: InputObject, gameProcessedEvent: boolean) 
		if gameProcessedEvent then return end
		
		if References[HighestSplit] and input.KeyCode.Name == References[HighestSplit] then
			SplitIncrement()
		elseif input.KeyCode.Name == "R" then
			CanReset = true
		end
	end)

	local Connection2 = LocalPlayer.Chatted:Connect(function(message: string, recipient: Player) 
		if message == "Nice!" and HighestSplit == 4 then
			SplitIncrement()
		end	
	end)
	
	repeat task.wait() until HighestSplit >= 6
	warn("RUN COMPLETE! Resetting when R is pressed.")
	print(`ENGINE TIME: {os.clock()-GameTime}`)
  Connection2:Disconnect()
	repeat task.wait() until CanReset
  Connection1:Disconnect()
end

