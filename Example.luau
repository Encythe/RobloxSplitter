local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")
local UIS = game:GetService("UserInputService")

local LocalPlayer = Players.LocalPlayer

local RobloxSplitter = require(ReplicatedStorage.RobloxSplitter)

while true do
	RobloxSplitter.Reset()
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
	RobloxSplitter.Start()
	
	local HighestSplit = 0
	local CanReset = false
	
	local Connection1 = UIS.InputBegan:Connect(function(input: InputObject, gameProcessedEvent: boolean) 
		if gameProcessedEvent then return end
		
		if input.KeyCode.Name == "W" then
			RobloxSplitter.Split(1)
			HighestSplit = 1
		elseif input.KeyCode.Name == "A" then
			RobloxSplitter.Split(2)
			HighestSplit = 2
		elseif input.KeyCode.Name == "S" then
			RobloxSplitter.Split(3)
			HighestSplit = 3
		elseif input.KeyCode.Name == "D" then
			RobloxSplitter.Split(4)
			HighestSplit = 4
		elseif input.KeyCode.Name == "Space" then
			RobloxSplitter.Split(6)
			HighestSplit = 6
		elseif input.KeyCode.Name == "R" then
			CanReset = true
		end
	end)

	local Connection2 = LocalPlayer.Chatted:Connect(function(message: string, recipient: Player) 
		if message == "Nice!" then
			RobloxSplitter.Split(5)
			HighestSplit = 5
		end	
	end)
	
	repeat task.wait() until HighestSplit >= 6
	warn("RUN COMPLETE! Resetting when R is pressed.")
    Connection1:Disconnect()
    Connection2:Disconnect()
	repeat task.wait() until CanReset
end

