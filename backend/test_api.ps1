# PowerShell API Testing Script
# Paige's Inner Circle - API Testing

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Paige's Inner Circle - API Testing" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Base URL
$baseUrl = "http://localhost:8000"

# Test 1: Health Check
Write-Host "1. Testing Health Check..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/health" -Method Get
    Write-Host "✓ Health Check Passed" -ForegroundColor Green
    $response | ConvertTo-Json
} catch {
    Write-Host "✗ Health Check Failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 2: API Info
Write-Host "2. Testing API Info..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api" -Method Get
    Write-Host "✓ API Info Retrieved" -ForegroundColor Green
    $response | ConvertTo-Json
} catch {
    Write-Host "✗ API Info Failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 3: Auth Status
Write-Host "3. Testing Auth Status..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/auth/status" -Method Get
    Write-Host "✓ Auth Status Retrieved" -ForegroundColor Green
    $response | ConvertTo-Json
} catch {
    Write-Host "✗ Auth Status Failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 4: Current Event (Public)
Write-Host "4. Testing Current Event (Public)..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/events/current" -Method Get
    Write-Host "✓ Current Event Retrieved" -ForegroundColor Green
    $response | ConvertTo-Json
} catch {
    Write-Host "✗ Current Event Failed: $_" -ForegroundColor Red
    Write-Host "Note: This is expected if no event exists yet" -ForegroundColor Gray
}
Write-Host ""

# Test 5: Request Access (with test email)
Write-Host "5. Testing Request Access..." -ForegroundColor Yellow
Write-Host "Note: This will fail until we add a member to the database" -ForegroundColor Gray
$testEmail = "test@example.com"
$body = @{
    email = $testEmail
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/auth/request-access" `
        -Method Post `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "✓ Access Granted!" -ForegroundColor Green
    Write-Host "Token: $($response.access_token)" -ForegroundColor Cyan
    
    # Save token for next tests
    $global:authToken = $response.access_token
    
    $response | ConvertTo-Json
} catch {
    Write-Host "✗ Access Denied (Expected - no members in database)" -ForegroundColor Red
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Testing Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan