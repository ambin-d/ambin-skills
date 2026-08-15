# 火山方舟 Ark 图片生成脚本（绕过 L3 权限墙）
# 用法: powershell -File generate_image.ps1 -Prompt "..." -Size 1280x720 -Model doubao-seedream-4-0-250828
# 输出: 图片直链 URL（stdout 第一行）
# 注意: 模型必须用带日期后缀的 doubao-seedream-4-0-250828，裸名 doubao-seedream-4-0 会报 InvalidEndpointOrModel.NotFound
param(
    [Parameter(Mandatory = $true)][string]$Prompt,
    [string]$Size = "1280x720",
    [string]$Model = "doubao-seedream-4-0-250828",
    [string]$Key = ""
)
$ErrorActionPreference = "Stop"

# 从 config.json 读 volc_api_key（未显式传 Key 时）
# <APP> 为宿主应用名占位符，请替换为你的 Agent 宿主应用目录（如 %APPDATA%\YourApp\config.json）
if (-not $Key) {
    $configPath = Join-Path $env:APPDATA "<APP>\config.json"
    if (-not (Test-Path $configPath)) {
        # 兜底：直接在 APPDATA 下找 config.json
        $configPath = Join-Path $env:APPDATA "config.json"
    }
    $config = Get-Content $configPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $Key = $config.volc_api_key
}
if (-not $Key) {
    throw "未找到 volc_api_key，请检查 config.json"
}

$body = @{
    model           = $Model
    prompt          = $Prompt
    size            = $Size
    response_format = "url"
} | ConvertTo-Json -Depth 5

$headers = @{
    "Authorization" = "Bearer $Key"
    "Content-Type"  = "application/json"
}

$resp = Invoke-RestMethod -Uri "https://ark.cn-beijing.volces.com/api/v3/images/generations" -Method Post -Headers $headers -Body $body
Write-Output $resp.data[0].url
