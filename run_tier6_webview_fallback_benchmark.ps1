# PowerShell Script: Tier 6 WebView Fail-Closed & Fallback Policy Benchmark Runner
param (
    [string]$Mode = "tier6"
)

$Adb = "C:\Users\ASUS\AppData\Local\Android\Sdk\platform-tools\adb.exe"
if (-not (Test-Path $Adb)) {
    $Adb = "adb"
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " SECRETHANDLE - TIER 6 WEBVIEW & FALLBACK BENCHMARK RUNNER" -ForegroundColor Cyan
Write-Host " (WebView Fail-Closed Origin & Custom Canvas Fallback)    " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check connected device
Write-Host "`n[1/4] Checking connected Android device via ADB..." -ForegroundColor Yellow
$devLines = & $Adb devices
$connected = $false
foreach ($line in $devLines) {
    if ($line -match "\bdevice\b" -and $line -notmatch "List of devices") {
        $connected = $true
        break
    }
}

if (-not $connected) {
    Write-Host "[-] ERROR: Khong tim thay thiet bi Android nao qua ADB!" -ForegroundColor Red
    exit 1
}

$model = (& $Adb shell getprop ro.product.model).Trim()
$brand = (& $Adb shell getprop ro.product.brand).Trim()
$version = (& $Adb shell getprop ro.build.version.release).Trim()
$sdk = (& $Adb shell getprop ro.build.version.sdk).Trim()
$fingerprint = (& $Adb shell getprop ro.build.fingerprint).Trim()

Write-Host "[+] Connected Device: $brand $model (Android $version, API $sdk)" -ForegroundColor Green

# 2. Check/Build APK
$ApkPath = "$PSScriptRoot\device\b3-secrethandle\build\b3secrethandle.apk"
if (-not (Test-Path $ApkPath)) {
    Write-Host "`n[2/4] Building b3secrethandle.apk..." -ForegroundColor Yellow
    powershell -ExecutionPolicy Bypass -File "$PSScriptRoot\device\b3-secrethandle\build_windows.ps1"
} else {
    Write-Host "`n[2/4] APK ready: $ApkPath" -ForegroundColor Green
}

# 3. Push and execute
Write-Host "`n[3/4] Pushing benchmark runner to /data/local/tmp/bench.jar..." -ForegroundColor Yellow
& $Adb push $ApkPath /data/local/tmp/bench.jar
& $Adb install -r -g $ApkPath

Write-Host "`n[4/4] Executing Tier 6 Benchmarks inside Android runtime (app_process)..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"

# 4a. Run WebView Fail-Closed Benchmark
Write-Host "  -> Running WebView Fail-Closed benchmark..." -ForegroundColor Cyan
$rawWebOutput = & $Adb shell "CLASSPATH=/data/local/tmp/bench.jar app_process /data/local/tmp com.secrethandle.b3.BenchmarkRunner webview"

# 4b. Run Fallback Policy Benchmark
Write-Host "  -> Running Fallback Policy benchmark..." -ForegroundColor Cyan
$rawFallbackOutput = & $Adb shell "CLASSPATH=/data/local/tmp/bench.jar app_process /data/local/tmp com.secrethandle.b3.BenchmarkRunner fallback"

# Format and save output
$outputDir = "$PSScriptRoot\output"
if (-not (Test-Path $outputDir)) { New-Item -ItemType Directory -Path $outputDir | Out-Null }

$webFile = "$outputDir\webview_failclosed_benchmark.json"
$fallbackFile = "$outputDir\fallback_policy_benchmark.json"

$wrappedWeb = @"
{
  "timestamp": "$timestamp",
  "device": {
    "brand": "$brand",
    "model": "$model",
    "android_version": "$version",
    "api_level": "$sdk",
    "fingerprint": "$fingerprint"
  },
  "benchmark_result": $rawWebOutput
}
"@

$wrappedFallback = @"
{
  "timestamp": "$timestamp",
  "device": {
    "brand": "$brand",
    "model": "$model",
    "android_version": "$version",
    "api_level": "$sdk",
    "fingerprint": "$fingerprint"
  },
  "benchmark_result": $rawFallbackOutput
}
"@

$wrappedWeb | Out-File -Encoding utf8 $webFile
$wrappedFallback | Out-File -Encoding utf8 $fallbackFile

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host " HOAN TAT THU NGHIEM TIER 6 THANH CONG!                  " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "[+] WebView Fail-Closed log: $webFile" -ForegroundColor Cyan
Write-Host "[+] Fallback Policy log:    $fallbackFile" -ForegroundColor Cyan

