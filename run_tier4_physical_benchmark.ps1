# PowerShell Script: Tier 4 Physical Device Benchmark Runner
# Measures real hardware Keystore latency and battery stats via ADB.
param (
    [string]$Mode = "all"
)

$Adb = "C:\Users\ASUS\AppData\Local\Android\Sdk\platform-tools\adb.exe"
if (-not (Test-Path $Adb)) {
    $Adb = "adb"
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " SECRETHANDLE - TIER 4 PHYSICAL DEVICE BENCHMARK RUNNER   " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check connected device
Write-Host "`n[1/6] Checking connected Android device via ADB..." -ForegroundColor Yellow
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
    Write-Host "    1. Cam cap USB noi dien thoai (Pixel/Samsung/Xiaomi...) voi may tinh."
    Write-Host "    2. Bat 'Tuy chon cho nha phat trien' (Developer Options) -> Bat 'Go loi USB' (USB Debugging)."
    Write-Host "    3. Mo khoa man hinh va chon 'Cho phep go loi USB tu may tinh nay'."
    exit 1
}

$model = (& $Adb shell getprop ro.product.model).Trim()
$brand = (& $Adb shell getprop ro.product.brand).Trim()
$version = (& $Adb shell getprop ro.build.version.release).Trim()
$sdk = (& $Adb shell getprop ro.build.version.sdk).Trim()
$fingerprint = (& $Adb shell getprop ro.build.fingerprint).Trim()

Write-Host "[+] Connected Device:" -ForegroundColor Green
Write-Host "    - Model: $brand $model"
Write-Host "    - Android Version: $version (API level $sdk)"
Write-Host "    - Build: $fingerprint"

# 2. Check or build APK
$ApkPath = "$PSScriptRoot\device\b3-secrethandle\build\b3secrethandle.apk"
if (-not (Test-Path $ApkPath)) {
    Write-Host "`n[2/6] Building b3secrethandle.apk..." -ForegroundColor Yellow
    powershell -ExecutionPolicy Bypass -File "$PSScriptRoot\device\b3-secrethandle\build_windows.ps1"
} else {
    Write-Host "`n[2/6] APK ready: $ApkPath" -ForegroundColor Green
}

# 3. Push benchmark runner to device
Write-Host "`n[3/6] Pushing benchmark runner to /data/local/tmp/bench.jar..." -ForegroundColor Yellow
& $Adb push $ApkPath /data/local/tmp/bench.jar
& $Adb install -r -g $ApkPath

# 4. Initialize battery stats
Write-Host "`n[4/6] Initializing battery measurement (dumpsys batterystats)..." -ForegroundColor Yellow
& $Adb shell dumpsys batterystats --reset
# Simulate unplugging power while keeping USB debugging active
& $Adb shell dumpsys battery unplug
Write-Host "[+] Battery stats reset and simulated unplug." -ForegroundColor Green

# 5. Execute benchmark inside Android runtime
Write-Host "`n[5/6] Executing BenchmarkRunner inside Android runtime (app_process)..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
$rawOutput = & $Adb shell "CLASSPATH=/data/local/tmp/bench.jar app_process /data/local/tmp com.secrethandle.b3.BenchmarkRunner $Mode"

# 6. Capture battery stats and restore battery charging
Write-Host "`n[6/6] Collecting battery stats and CPU profiling..." -ForegroundColor Yellow
$batteryDump = & $Adb shell dumpsys batterystats com.secrethandle.b3
$cpuDump = & $Adb shell dumpsys cpuinfo
& $Adb shell dumpsys battery reset

# Format and save output
$outputDir = "$PSScriptRoot\output"
if (-not (Test-Path $outputDir)) { New-Item -ItemType Directory -Path $outputDir | Out-Null }
$resultFile = "$outputDir\physical_device_benchmark.json"

$cpuSummary = ($cpuDump | Select-String -Pattern "secrethandle|TOTAL") -join "; "

$wrappedOutput = @"
{
  "timestamp": "$timestamp",
  "physical_device": {
    "brand": "$brand",
    "model": "$model",
    "android_version": "$version",
    "api_level": "$sdk",
    "fingerprint": "$fingerprint"
  },
  "benchmark_result": $rawOutput,
  "cpu_sample": "$cpuSummary"
}
"@

$wrappedOutput | Out-File -Encoding utf8 $resultFile

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host " HOAN TAT DO DAC TREN THIET BI VAT LY THANH CONG!         " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "JSON Result saved to: $resultFile" -ForegroundColor Cyan
Write-Host "`nFirst lines of output:" -ForegroundColor Yellow
Get-Content $resultFile | Select-Object -First 35
