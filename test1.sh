# FortiGate 配置信息
$FORTIGATE_IP = "192.168.1.1"
$API_USER = "api1"
$ADMIN_USER = "admin"
$ADMIN_PASSWORD = "test123"  # 建议从安全存储读取

# 忽略 SSL 证书验证（仅测试环境）
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }

# Step 1: 管理员登录并获取 CSRF Token
Write-Host "Logging in..."
$loginUrl = "https://${FORTIGATE_IP}/logincheck"
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$loginResponse = Invoke-WebRequest -Uri $loginUrl `
  -Method POST `
  -Body "username=${ADMIN_USER}&secretkey=${ADMIN_PASSWORD}" `
  -ContentType "application/x-www-form-urlencoded" `
  -WebSession $session `
  -UseBasicParsing

# 提取 CSRF Token
$csrfToken = $session.Cookies.GetCookies($loginUrl) | Where-Object { $_.Name -eq "ccsrftoken" } | Select-Object -ExpandProperty Value
$csrfToken = $csrfToken.Trim('"')

# Step 2: 创建 API 用户
Write-Host "Creating API user ${API_USER}..."
$createUserUrl = "https://${FORTIGATE_IP}/api/v2/cmdb/system/api-user"
$userBody = @{
  name = $API_USER
  accprofile = "super_admin"
  vdom = "root"
  cors_allow_origin = "*"
  comments = "API User for automation"
  force_password_change = "disable"
  two_factor = "disable"
  rpc_permit = "read-write"
  accprofile_override = "enable"
} | ConvertTo-Json

Invoke-RestMethod -Uri $createUserUrl `
  -Method POST `
  -Headers @{ "X-CSRFTOKEN" = $csrfToken } `
  -WebSession $session `
  -ContentType "application/json" `
  -Body $userBody `
  -UseBasicParsing | Out-Null

# Step 3: 生成 API 密钥
Write-Host "Generating API key..."
$generateKeyUrl = "https://${FORTIGATE_IP}/api/v2/monitor/system/api-user/generate-key"
$keyBody = @{ "api-user" = $API_USER } | ConvertTo-Json

$keyResponse = Invoke-RestMethod -Uri $generateKeyUrl `
  -Method POST `
  -Headers @{ "X-CSRFTOKEN" = $csrfToken } `
  -WebSession $session `
  -ContentType "application/json" `
  -Body $keyBody `
  -UseBasicParsing

# 提取并保存 API 密钥
$API_KEY = $keyResponse.results.access_token
$API_KEY | Out-File -FilePath "api_key.txt" -Encoding UTF8
Write-Host "API key saved to api_key.txt"

# Step 4: 测试 API 密钥
Write-Host "Testing API connection..."
$testUrl = "https://${FORTIGATE_IP}/api/v2/monitor/system/status"
$testResponse = Invoke-RestMethod -Uri $testUrl `
  -Headers @{ "Authorization" = "Bearer $API_KEY" } `
  -UseBasicParsing

Write-Host "API test response:"
$testResponse | Format-List

# 清理会话
$session = $null
Write-Host "Done!"