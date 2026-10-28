print("[aimbot] iniciando...")

local hasDrawing = (type(Drawing) == "table") and (type(Drawing.new) == "function")

local Players          = game:GetService("Players")
local RunService       = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local Workspace        = game:GetService("Workspace")
local TweenService     = game:GetService("TweenService")
local Lighting         = game:GetService("Lighting")

local lp = Players.LocalPlayer
local pg = lp:WaitForChild("PlayerGui", 10)
if not pg then warn("[aimbot] PlayerGui não apareceu"); return end

if not lp.Character then
    lp.CharacterAdded:Wait()
end

local camera = Workspace.CurrentCamera

local WHITE = Color3.fromRGB(245,245,245)
local BLACK = Color3.fromRGB(8,8,8)
local GREY  = Color3.fromRGB(30,30,30)
local MID   = Color3.fromRGB(110,110,110)

local CFG = {
    key=Enum.KeyCode.E, menuKey=Enum.KeyCode.RightShift,
    fovRadius=160, smoothness=0.18, maxStepDeg=5.0, jitterPx=1,
    aimPartNames={"Head","HumanoidRootPart","UpperTorso","Torso"},
    teamCheck=true, wallbang=true, fovVisible=true, aimEnabled=false,
    penetrable = {
        [Enum.Material.Wood]          = true,
        [Enum.Material.WoodPlanks]    = true,
        [Enum.Material.Glass]         = true,
        [Enum.Material.Plastic]       = true,
        [Enum.Material.SmoothPlastic] = true,
        [Enum.Material.Fabric]        = true,
        [Enum.Material.Carpet]        = true,
        [Enum.Material.Grass]         = true,
    },
    maxPenetrationStuds=2.0,
}

local gui = Instance.new("ScreenGui")
gui.Name="AimMenu"; gui.ResetOnSpawn=false; gui.IgnoreGuiInset=true
gui.DisplayOrder=999; gui.Parent=pg

local splash = Instance.new("Frame")
splash.Size=UDim2.new(1,0,1,0); splash.BackgroundColor3=BLACK
splash.BorderSizePixel=0; splash.ZIndex=50; splash.Parent=gui

local brand = Instance.new("TextLabel")
brand.Size=UDim2.new(1,0,0,40); brand.Position=UDim2.new(0,0,0.5,-110)
brand.BackgroundTransparency=1; brand.Text="AIMBOT"
brand.Font=Enum.Font.GothamBlack; brand.TextSize=44
brand.TextColor3=WHITE; brand.TextTransparency=1; brand.ZIndex=51; brand.Parent=splash

local sub = Instance.new("TextLabel")
sub.Size=UDim2.new(1,0,0,20); sub.Position=UDim2.new(0,0,0.5,-66)
sub.BackgroundTransparency=1; sub.Text="c o n t r o l   s y s t e m"
sub.Font=Enum.Font.Gotham; sub.TextSize=12; sub.TextColor3=MID
sub.TextTransparency=1; sub.ZIndex=51; sub.Parent=splash

local divider = Instance.new("Frame")
divider.Size=UDim2.new(0,0,0,1); divider.Position=UDim2.new(0.5,0,0.5,-30)
divider.AnchorPoint=Vector2.new(0.5,0); divider.BackgroundColor3=WHITE
divider.BackgroundTransparency=1; divider.BorderSizePixel=0
divider.ZIndex=51; divider.Parent=splash

local enterBtn = Instance.new("TextButton")
enterBtn.Size=UDim2.new(0,200,0,52); enterBtn.Position=UDim2.new(0.5,0,0.5,20)
enterBtn.AnchorPoint=Vector2.new(0.5,0); enterBtn.BackgroundColor3=WHITE
enterBtn.BackgroundTransparency=1; enterBtn.Text="ENTER"
enterBtn.Font=Enum.Font.GothamBold; enterBtn.TextSize=16
enterBtn.TextColor3=BLACK; enterBtn.TextTransparency=1
enterBtn.BorderSizePixel=0; enterBtn.AutoButtonColor=false
enterBtn.ZIndex=52; enterBtn.Parent=splash
Instance.new("UICorner", enterBtn).CornerRadius=UDim.new(0,6)
local enterStroke = Instance.new("UIStroke")
enterStroke.Color=WHITE; enterStroke.Thickness=1.5
enterStroke.Transparency=1; enterStroke.Parent=enterBtn

task.spawn(function()
    local t = TweenInfo.new(0.4, Enum.EasingStyle.Quint, Enum.EasingDirection.Out)
    TweenService:Create(brand, t, {TextTransparency=0}):Play(); task.wait(0.1)
    TweenService:Create(sub, t, {TextTransparency=0}):Play()
    TweenService:Create(divider, t, {BackgroundTransparency=0.3, Size=UDim2.new(0,200,0,1)}):Play()
    task.wait(0.15)
    TweenService:Create(enterBtn, t, {BackgroundTransparency=0, TextTransparency=0}):Play()
    TweenService:Create(enterStroke, t, {Transparency=0}):Play()
end)

enterBtn.MouseEnter:Connect(function()
    TweenService:Create(enterBtn, TweenInfo.new(0.15), {BackgroundTransparency=0.15}):Play()
end)
enterBtn.MouseLeave:Connect(function()
    TweenService:Create(enterBtn, TweenInfo.new(0.15), {BackgroundTransparency=0}):Play()
end)

local menuBuilt = false
local menuOpen = false
local panel, layout, stroke, title, titleLine, dragBar

local function buildMenu()
    if menuBuilt then return end
    menuBuilt = true
    
    panel = Instance.new("Frame")
    panel.Size=UDim2.new(0,0,0,0); panel.Position=UDim2.new(0.5,-160,0.5,-140)
    panel.BackgroundColor3=BLACK; panel.BackgroundTransparency=0.05
    panel.BorderSizePixel=0; panel.ClipsDescendants=true
    panel.Visible=true; panel.ZIndex=20; panel.Parent=gui
    Instance.new("UICorner", panel).CornerRadius=UDim.new(0,10)

    stroke = Instance.new("UIStroke")
    stroke.Color=WHITE; stroke.Thickness=1.2
    stroke.Transparency=0.4; stroke.Parent=panel

    title = Instance.new("TextLabel")
    title.Size=UDim2.new(1,0,0,44); title.BackgroundTransparency=1
    title.Text="AIMBOT // CONTROL"; title.Font=Enum.Font.GothamBold
    title.TextSize=15; title.TextColor3=WHITE; title.ZIndex=21; title.Parent=panel

    dragBar = Instance.new("TextButton")
    dragBar.Size=UDim2.new(1,0,0,44); dragBar.BackgroundTransparency=1
    dragBar.Text=""; dragBar.ZIndex=22; dragBar.Parent=panel

    titleLine = Instance.new("Frame")
    titleLine.Size=UDim2.new(1,-24,0,1); titleLine.Position=UDim2.new(0,12,0,44)
    titleLine.BackgroundColor3=WHITE; titleLine.BackgroundTransparency=0.6
    titleLine.BorderSizePixel=0; titleLine.ZIndex=21; titleLine.Parent=panel

    local list = Instance.new("Frame")
    list.Size=UDim2.new(1,-24,0,0); list.Position=UDim2.new(0,12,0,52)
    list.BackgroundTransparency=1; list.ZIndex=21; list.Parent=panel
    layout = Instance.new("UIListLayout")
    layout.Padding=UDim.new(0,8); layout.SortOrder=Enum.SortOrder.LayoutOrder
    layout.Parent=list

    local function makeToggle(text, getter, setter)
        local row = Instance.new("Frame")
        row.Size=UDim2.new(1,0,0,34); row.BackgroundColor3=GREY
        row.BackgroundTransparency=0.15; row.BorderSizePixel=0
        row.ZIndex=21; row.Parent=list
        Instance.new("UICorner", row).CornerRadius=UDim.new(0,6)
        local label = Instance.new("TextLabel")
        label.Size=UDim2.new(1,-60,1,0); label.Position=UDim2.new(0,12,0,0)
        label.BackgroundTransparency=1; label.Text=text
        label.Font=Enum.Font.Gotham; label.TextSize=13; label.TextColor3=WHITE
        label.TextXAlignment=Enum.TextXAlignment.Left; label.ZIndex=22; label.Parent=row
        local dot = Instance.new("Frame")
        dot.Size=UDim2.new(0,36,0,18); dot.Position=UDim2.new(1,-48,0.5,-9)
        dot.BackgroundColor3 = getter() and WHITE or Color3.fromRGB(60,60,60)
        dot.BorderSizePixel=0; dot.ZIndex=22; dot.Parent=row
        Instance.new("UICorner", dot).CornerRadius=UDim.new(1,0)
        local knob = Instance.new("Frame")
        knob.Size=UDim2.new(0,14,0,14)
        knob.Position = getter() and UDim2.new(1,-16,0.5,-7) or UDim2.new(0,2,0.5,-7)
        knob.BackgroundColor3 = getter() and BLACK or WHITE
        knob.BorderSizePixel=0; knob.ZIndex=23; knob.Parent=dot
        Instance.new("UICorner", knob).CornerRadius=UDim.new(1,0)
        local btn = Instance.new("TextButton")
        btn.Size=UDim2.new(1,0,1,0); btn.BackgroundTransparency=1
        btn.Text=""; btn.ZIndex=24; btn.Parent=row
        btn.MouseButton1Click:Connect(function()
            setter(not getter()); local on = getter()
            TweenService:Create(dot, TweenInfo.new(0.2),
                {BackgroundColor3 = on and WHITE or Color3.fromRGB(60,60,60)}):Play()
            TweenService:Create(knob, TweenInfo.new(0.2),
                {Position = on and UDim2.new(1,-16,0.5,-7) or UDim2.new(0,2,0.5,-7),
                 BackgroundColor3 = on and BLACK or WHITE}):Play()
        end)
    end

    local function makeSlider(text, min, max, getter, setter)
        local row = Instance.new("Frame")
        row.Size=UDim2.new(1,0,0,40); row.BackgroundColor3=GREY
        row.BackgroundTransparency=0.15; row.BorderSizePixel=0
        row.ZIndex=21; row.Parent=list
        Instance.new("UICorner", row).CornerRadius=UDim.new(0,6)
        local label = Instance.new("TextLabel")
        label.Size=UDim2.new(1,-20,0,18); label.Position=UDim2.new(0,12,0,4)
        label.BackgroundTransparency=1
        label.Text = text .. "  [" .. tostring(getter()) .. "]"
        label.Font=Enum.Font.Gotham; label.TextSize=12; label.TextColor3=WHITE
        label.TextXAlignment=Enum.TextXAlignment.Left; label.ZIndex=22; label.Parent=row
        local track = Instance.new("Frame")
        track.Size=UDim2.new(1,-24,0,4); track.Position=UDim2.new(0,12,0,28)
        track.BackgroundColor3=Color3.fromRGB(70,70,70); track.BorderSizePixel=0
        track.ZIndex=22; track.Parent=row
        Instance.new("UICorner", track).CornerRadius=UDim.new(1,0)
        local fill = Instance.new("Frame")
        local pct = (getter()-min)/(max-min)
        fill.Size=UDim2.new(pct,0,1,0); fill.BackgroundColor3=WHITE
        fill.BorderSizePixel=0; fill.ZIndex=23; fill.Parent=track
        Instance.new("UICorner", fill).CornerRadius=UDim.new(1,0)
        local btn = Instance.new("TextButton")
        btn.Size=UDim2.new(1,0,1,0); btn.BackgroundTransparency=1
        btn.Text=""; btn.ZIndex=24; btn.Parent=row
        local function setFromX(ax)
            local w = track.AbsoluteSize.X
            local rel = math.clamp((ax - track.AbsolutePosition.X)/w, 0, 1)
            local v = math.floor(min + (max-min)*rel)
            setter(v); fill.Size=UDim2.new(rel,0,1,0)
            label.Text = text .. "  [" .. tostring(v) .. "]"
        end
        btn.MouseButton1Click:Connect(function()
            setFromX(UserInputService:GetMouseLocation().X)
        end)
        btn.TouchTap:Connect(function(touches)
            if touches and #touches > 0 then setFromX(touches[1].Position.X) end
        end)
    end

    makeToggle("Enable Aimbot", function() return CFG.aimEnabled end, function(v) CFG.aimEnabled=v end)
    makeToggle("Team Check",   function() return CFG.teamCheck end, function(v) CFG.teamCheck=v end)
    makeToggle("Wallbang",     function() return CFG.wallbang end, function(v) CFG.wallbang=v end)
    makeToggle("Show FOV",     function() return CFG.fovVisible end, function(v) CFG.fovVisible=v end)
    makeSlider("FOV Radius", 60, 400, function() return CFG.fovRadius end, function(v) CFG.fovRadius=v end)
    makeSlider("Smoothness x100", 1, 50,
        function() return math.floor(CFG.smoothness*100) end,
        function(v) CFG.smoothness=v/100 end)

    local ti = TweenInfo.new(0.35, Enum.EasingStyle.Quint, Enum.EasingDirection.Out)
    TweenService:Create(panel, ti, {
        Size=UDim2.new(0,320,0,52+layout.AbsoluteContentSize.Y+16),
        BackgroundTransparency=0.05}):Play()

    local dragging, dragStart, startPos = false, nil, nil
    dragBar.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1
        or input.UserInputType == Enum.UserInputType.Touch then
            dragging = true
            dragStart = Vector2.new(input.Position.X, input.Position.Y)
            startPos = panel.Position
        end
    end)
    UserInputService.InputChanged:Connect(function(input)
        if dragging and (input.UserInputType == Enum.UserInputType.MouseMovement
        or input.UserInputType == Enum.UserInputType.Touch) then
            local p = Vector2.new(input.Position.X, input.Position.Y)
            local d = p - dragStart
            panel.Position = UDim2.new(
                startPos.X.Scale, startPos.X.Offset + d.X,
                startPos.Y.Scale, startPos.Y.Offset + d.Y)
        end
    end)
    UserInputService.InputEnded:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1
        or input.UserInputType == Enum.UserInputType.Touch then dragging = false end
    end)
end

if hasDrawing then
    local fovCircle = Drawing.new("Circle")
    fovCircle.Thickness=1.5; fovCircle.Color=WHITE
    fovCircle.Filled=false; fovCircle.Transparency=0.85; fovCircle.Visible=false
    RunService.RenderStepped:Connect(function()
        if CFG.fovVisible and CFG.aimEnabled then
            fovCircle.Visible=true; fovCircle.Radius=CFG.fovRadius
            fovCircle.Position=Vector2.new(camera.ViewportSize.X/2, camera.ViewportSize.Y/2)
        else
            fovCircle.Visible=false
        end
    end)
end

local fab = Instance.new("TextButton")
fab.Size=UDim2.new(0,48,0,48); fab.Position=UDim2.new(1,-70,0.5,0)
fab.BackgroundColor3=BLACK; fab.BackgroundTransparency=0.1
fab.Text="☰"; fab.Font=Enum.Font.GothamBold; fab.TextSize=22
fab.TextColor3=WHITE; fab.BorderSizePixel=0; fab.AutoButtonColor=false
fab.ZIndex=40; fab.Visible=false; fab.Parent=gui
Instance.new("UICorner", fab).CornerRadius=UDim.new(1,0)
local fabStroke = Instance.new("UIStroke")
fabStroke.Color=WHITE; fabStroke.Thickness=1.5
fabStroke.Transparency=0.4; fabStroke.Parent=fab

task.delay(0.55, function() fab.Visible = true end)

fab.MouseButton1Click:Connect(function()
    if not panel then return end
    if menuOpen then
        menuOpen = false
        panel.Visible = false
    else
        menuOpen = true
        panel.Visible = true
    end
end)

if UserInputService.KeyboardEnabled then
    UserInputService.InputBegan:Connect(function(input, processed)
        if processed then return end
        if input.KeyCode == CFG.menuKey then
            if panel then
                menuOpen = not menuOpen
                panel.Visible = menuOpen
            end
        elseif input.KeyCode == CFG.key then
            CFG.aimEnabled = not CFG.aimEnabled
        end
    end)
end

local fabDrag, fabStart, fabPos = false, nil, nil
fab.InputBegan:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.Touch
    or input.UserInputType == Enum.UserInputType.MouseButton1 then
        fabDrag = true; fabStart = Vector2.new(input.Position.X, input.Position.Y)
        fabPos = fab.Position
    end
end)
UserInputService.InputChanged:Connect(function(input)
    if fabDrag then
        local p = Vector2.new(input.Position.X, input.Position.Y)
        local d = p - fabStart
        if d.Magnitude > 5 then
            fab.Position = UDim2.new(
                fabPos.X.Scale, fabPos.X.Offset + d.X,
                fabPos.Y.Scale, fabPos.Y.Offset + d.Y)
        end
    end
end)
UserInputService.InputEnded:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.Touch
    or input.UserInputType == Enum.UserInputType.MouseButton1 then
        fabDrag = false
    end
end)

local function pressEnter()
    TweenService:Create(splash, TweenInfo.new(0.45, Enum.EasingStyle.Quint),
        {BackgroundTransparency=1}):Play()
    TweenService:Create(brand, TweenInfo.new(0.3), {TextTransparency=1}):Play()
    TweenService:Create(sub, TweenInfo.new(0.3), {TextTransparency=1}):Play()
    TweenService:Create(divider, TweenInfo.new(0.3),
        {BackgroundTransparency=1, Size=UDim2.new(0,0,0,1)}):Play()
    TweenService:Create(enterBtn, TweenInfo.new(0.3),
        {BackgroundTransparency=1, TextTransparency=1}):Play()
    TweenService:Create(enterStroke, TweenInfo.new(0.3), {Transparency=1}):Play()
    task.delay(0.5, function() 
        splash.Visible = false 
        buildMenu()
        menuOpen = true
    end)
end

enterBtn.MouseButton1Click:Connect(pressEnter)
enterBtn.TouchTap:Connect(pressEnter)

local function isAlive(char)
    if not char then return false end
    local h = char:FindFirstChildOfClass("Humanoid")
    return h and h.Health > 0
end

local function getAimPart(char)
    for _, n in ipairs(CFG.aimPartNames) do
        local p = char:FindFirstChild(n)
        if p and p:IsA("BasePart") then return p end
    end
    for _, d in ipairs(char:GetDescendants()) do
        if d:IsA("BasePart") then return d end
    end
end

local function canSee(from, to, char)
    local params = RaycastParams.new()
    params.FilterType = Enum.RaycastFilterType.Exclude
    params.FilterDescendantsInstances = {lp.Character, char}
    params.IgnoreWater = true
    local origin, dir = from, (to - from)
    local total = dir.Magnitude; dir = dir.Unit
    local traveled = 0
    while traveled < total do
        local r = Workspace:Raycast(origin, dir * (total - traveled), params)
        if not r then return true end
        if CFG.wallbang and CFG.penetrable[r.Material] then
            local seg = (r.Position - origin).Magnitude
            if seg > CFG.maxPenetrationStuds then return false end
            traveled = traveled + seg + 0.05
            origin = r.Position + dir * 0.05
        else
            return false
        end
    end
    return true
end

local function getTarget()
    local best, bestDist = nil, CFG.fovRadius
    local center = Vector2.new(camera.ViewportSize.X/2, camera.ViewportSize.Y/2)
    for _, plr in ipairs(Players:GetPlayers()) do
        if plr ~= lp and isAlive(plr.Character) then
            if not (CFG.teamCheck and plr.Team and lp.Team and plr.Team == lp.Team) then
                local part = getAimPart(plr.Character)
                if part then
                    local sp, on = camera:WorldToViewportPoint(part.Position)
                    if on then
                        local d = (Vector2.new(sp.X, sp.Y) - center).Magnitude
                        if d < bestDist and canSee(camera.CFrame.Position, part.Position, plr.Character) then
                            bestDist = d; best = part
                        end
                    end
                end
            end
        end
    end
    return best
end

local function aimAt(part)
    local camPos = camera.CFrame.Position
    local curDir = camera.CFrame.LookVector
    local tgtDir = (part.Position - camPos).Unit
    local dot = math.clamp(curDir:Dot(tgtDir), -1, 1)
    local angDeg = math.deg(math.acos(dot))
    local step = math.min(CFG.maxStepDeg, angDeg) / math.max(angDeg, 1e-3)
    local jx = (math.random()-0.5) * CFG.jitterPx / 1000
    local jy = (math.random()-0.5) * CFG.jitterPx / 1000
    local target = CFrame.lookAt(camPos, camPos + curDir:Lerp(tgtDir, step))
    camera.CFrame = camera.CFrame:Lerp(target * CFrame.Angles(jy, jx, 0), CFG.smoothness)
end

Workspace:GetPropertyChangedSignal("CurrentCamera"):Connect(function()
    camera = Workspace.CurrentCamera
end)

RunService.RenderStepped:Connect(function()
    if CFG.aimEnabled and isAlive(lp.Character) then
        local t = getTarget()
        if t then aimAt(t) end
    end
end)
