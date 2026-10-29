# PowerShell build script for B3 SecretHandle on Windows
$ErrorActionPreference = "Stop"

$SdkDir = "C:\Users\ASUS\AppData\Local\Android\Sdk"
$BuildTools = "$SdkDir\build-tools\35.0.0"
$AndroidJar = "$SdkDir\platforms\android-34\android.jar"
$JbrHome = "C:\Program Files\Android\Android Studio\jbr"
$JbrBin = "$JbrHome\bin"
$env:JAVA_HOME = $JbrHome
$env:PATH = "$JbrBin;$env:PATH"

$RootDir = "$PSScriptRoot"
$BuildDir = "$RootDir\build"

Write-Host "== 0. Checking toolchain =="
& "$JbrBin\javac.exe" -version
& "$JbrBin\java.exe" -version

if (Test-Path "$BuildDir") {
    Remove-Item -Recurse -Force "$BuildDir"
}
New-Item -ItemType Directory -Force -Path "$BuildDir\classes" | Out-Null
New-Item -ItemType Directory -Force -Path "$BuildDir\dex" | Out-Null

Write-Host "== 1. aapt2 compile + link =="
& "$BuildTools\aapt2.exe" compile --dir "$RootDir\android\res" -o "$BuildDir\res.zip"
& "$BuildTools\aapt2.exe" link -o "$BuildDir\base.apk" -I "$AndroidJar" `
  --manifest "$RootDir\android\AndroidManifest.xml" `
  "$BuildDir\res.zip" `
  --min-sdk-version 24 --target-sdk-version 34 `
  --version-code 1 --version-name "0.1"

Write-Host "== 2. javac =="
$srcFiles = Get-ChildItem -Recurse -Path "$RootDir\android\src" -Filter "*.java" | ForEach-Object { $_.FullName }
& "$JbrBin\javac.exe" -source 8 -target 8 -encoding UTF-8 -nowarn `
  -bootclasspath "$AndroidJar" -d "$BuildDir\classes" $srcFiles

Write-Host "== 3. jar =="
Push-Location "$BuildDir\classes"
& "$JbrBin\jar.exe" cf "$BuildDir\classes.jar" .
Pop-Location

Write-Host "== 4. d8 =="
& "$JbrBin\java.exe" -cp "$BuildTools\lib\d8.jar" com.android.tools.r8.D8 `
  --min-api 24 --lib "$AndroidJar" --output "$BuildDir\dex" "$BuildDir\classes.jar"

Write-Host "== 5. package dex into apk =="
python -c @"
import zipfile, sys
apk = r'$BuildDir\base.apk'
dex = r'$BuildDir\dex\classes.dex'
tmp = apk + '.tmp'
with zipfile.ZipFile(apk) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        if item.filename == 'classes.dex': continue
        zout.writestr(item, zin.read(item.filename))
    zi = zipfile.ZipInfo('classes.dex', date_time=(1980, 1, 1, 0, 0, 0))
    zi.compress_type = zipfile.ZIP_DEFLATED
    zi.external_attr = 0o644 << 16
    with open(dex, 'rb') as fh:
        zout.writestr(zi, fh.read())
import os
os.replace(tmp, apk)
"@

Write-Host "== 6. zipalign =="
& "$BuildTools\zipalign.exe" -f -p 4 "$BuildDir\base.apk" "$BuildDir\aligned.apk"

Write-Host "== 7. apksigner =="
& "$BuildTools\apksigner.bat" sign --ks "$RootDir\debug.keystore" `
  --ks-pass pass:android --key-pass pass:android `
  --ks-key-alias androiddebugkey `
  --out "$BuildDir\b3secrethandle.apk" "$BuildDir\aligned.apk"

& "$BuildTools\apksigner.bat" verify "$BuildDir\b3secrethandle.apk"

Write-Host "BUILT SUCCESSFULLY -> $BuildDir\b3secrethandle.apk"
