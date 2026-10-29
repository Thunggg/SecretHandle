# PowerShell Script: Tier 5 Extended Benchmark Runner (Segmented OTP & Clipboard Sources)
param (
    [string]$Mode = "extended"
)

$Adb = "C:\Users\ASUS\AppData\Local\Android\Sdk\platform-tools\adb.exe"
if (-not (Test-Path $Adb)) {
    $Adb = "adb"
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " SECRETHANDLE - TIER 5 EXTENDED BENCHMARK RUNNER         " -ForegroundColor Cyan
Write-Host " (Segmented 6-Digit OTP UI & Clipboard Source Mediation)  " -ForegroundColor Cyan
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
    Write-Host "[-] ERROR: Khong tim thay dien thoai Android nao ket noi qua ADB!" -ForegroundColor Red
    Write-Host "    Vui long kiem tra:" -ForegroundColor Yellow
    Write-Host "    1. Cam cap USB noi dien thoai (Samsung/Pixel...) voi may tinh."
    Write-Host "    2. Bat 'Tuy chon cho nha phat trien' (Developer Options) -> Bat 'Go loi USB' (USB Debugging)."
    Write-Host "    3. Mo khoa man hinh va chon 'Cho phep go loi USB tu may tinh nay'."
    exit 1
}

$model = (& $Adb shell getprop ro.product.model).Trim()
$brand = (& $Adb shell getprop ro.product.brand).Trim()
$version = (& $Adb shell getprop ro.build.version.release).Trim()
$sdk = (& $Adb shell getprop ro.build.version.sdk).Trim()

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

Write-Host "`n[4/4] Executing Extended Benchmark inside Android runtime (app_process)..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
$rawOutput = & $Adb shell "CLASSPATH=/data/local/tmp/bench.jar app_process /data/local/tmp com.secrethandle.b3.BenchmarkRunner $Mode"

# Format and save output
$outputDir = "$PSScriptRoot\output"
if (-not (Test-Path $outputDir)) { New-Item -ItemType Directory -Path $outputDir | Out-Null }
$resultFile = "$outputDir\extended_source_ui_benchmark.json"

$wrappedOutput = @"
{
  "timestamp": "$timestamp",
  "device": {
    "brand": "$brand",
    "model": "$model",
    "android_version": "$version",
    "api_level": "$sdk"
  },
  "benchmark_result": $rawOutput
}
"@

$wrappedOutput | Out-File -Encoding utf8 $resultFile

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host " HOAN TAT THU NGHIEM TIER 5 THANH CONG!                  " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "Ket qua luu tai: $resultFile" -ForegroundColor Cyan
Write-Host "`nKet qua chi tiet:" -ForegroundColor Yellow
Get-Content $resultFile | Select-Object -First 40
