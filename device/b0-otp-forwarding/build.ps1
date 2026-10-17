# Build the B0 harness APK without Gradle, using the Android SDK build-tools
# and Android Studio's bundled JDK (JBR).
#
# Java-based tools (javac, d8, apksigner, keytool, jar) are launched through
# Start-Process with redirected streams because calling them directly in some
# non-interactive shells hangs.

$ErrorActionPreference = 'Stop'

$root = $PSScriptRoot
$sdk  = Join-Path $env:LOCALAPPDATA 'Android\Sdk'
$jbr  = 'C:\Program Files\Android\Android Studio\jbr'
$java = Join-Path $jbr 'bin\java.exe'
$javac = Join-Path $jbr 'bin\javac.exe'
$keytool = Join-Path $jbr 'bin\keytool.exe'
$jartool = Join-Path $jbr 'bin\jar.exe'
$bt = Join-Path $sdk 'build-tools\35.0.0'
$aapt2 = Join-Path $bt 'aapt2.exe'
$zipalign = Join-Path $bt 'zipalign.exe'
$d8jar = Join-Path $bt 'lib\d8.jar'
$signerjar = Join-Path $bt 'lib\apksigner.jar'
$androidJar = Join-Path $sdk 'platforms\android-34\android.jar'

$androidDir = Join-Path $root 'android'
$manifest = Join-Path $androidDir 'AndroidManifest.xml'
$srcDir = Join-Path $androidDir 'src'
$build = Join-Path $root 'build'

Remove-Item -Recurse -Force $build -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $build | Out-Null

function Run-Proc {
    param([string]$File, [string[]]$ArgList, [string]$Tag)
    Write-Host "==> $Tag"
    $quoted = $ArgList | ForEach-Object { if ($_ -match '\s') { '"' + $_ + '"' } else { $_ } }
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $File
    $psi.Arguments = ($quoted -join ' ')
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $proc = [System.Diagnostics.Process]::Start($psi)
    $stdout = $proc.StandardOutput.ReadToEnd()
    $stderr = $proc.StandardError.ReadToEnd()
    if (-not $proc.WaitForExit(300000)) {
        try { $proc.Kill() } catch {}
        throw "$Tag timed out"
    }
    if ($stdout -and $stdout.Trim()) { Write-Host $stdout.Trim() }
    if ($stderr -and $stderr.Trim()) { Write-Host $stderr.Trim() }
    if ($proc.ExitCode -ne 0) { throw "$Tag failed with exit code $($proc.ExitCode)" }
}

# 1. link resources + manifest into a base APK
Run-Proc $aapt2 @(
    'link', '-o', (Join-Path $build 'base.apk'),
    '-I', $androidJar,
    '--manifest', $manifest,
    '--min-sdk-version', '24',
    '--target-sdk-version', '34',
    '--version-code', '1',
    '--version-name', '0.1'
) 'aapt2-link'

# 2. compile Java sources to Java 8 bytecode against android.jar
$classes = Join-Path $build 'classes'
New-Item -ItemType Directory -Force -Path $classes | Out-Null
$sources = Get-ChildItem -Recurse -Filter *.java $srcDir | ForEach-Object { $_.FullName }
$argfile = Join-Path $build 'javac.args'
$argLines = @(
    '-source', '8', '-target', '8', '-encoding', 'UTF-8', '-nowarn',
    '-bootclasspath', $androidJar,
    '-d', $classes
) + $sources
Set-Content -Path $argfile -Value $argLines -Encoding ASCII
Run-Proc $javac @("@" + $argfile) 'javac'

# 3. package classes into a jar for d8
$classesJar = Join-Path $build 'classes.jar'
Run-Proc $jartool @('cf', $classesJar, '-C', $classes, '.') 'jar'

# 4. convert to dex
$dexDir = Join-Path $build 'dex'
New-Item -ItemType Directory -Force -Path $dexDir | Out-Null
Run-Proc $java @(
    '-cp', $d8jar, 'com.android.tools.r8.D8',
    '--min-api', '24', '--lib', $androidJar,
    '--output', $dexDir, $classesJar
) 'd8'

# 5. add classes.dex into the base APK
Add-Type -AssemblyName System.IO.Compression.FileSystem
$apk = Join-Path $build 'base.apk'
$zip = [System.IO.Compression.ZipFile]::Open($apk, 'Update')
[System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, (Join-Path $dexDir 'classes.dex'), 'classes.dex') | Out-Null
$zip.Dispose()

# 6. align
$aligned = Join-Path $build 'aligned.apk'
Run-Proc $zipalign @('-f', '-p', '4', $apk, $aligned) 'zipalign'

# 7. debug keystore
$ks = Join-Path $root 'debug.keystore'
if (-not (Test-Path $ks)) {
    Run-Proc $keytool @(
        '-genkeypair', '-keystore', $ks,
        '-storepass', 'android', '-keypass', 'android',
        '-alias', 'androiddebugkey',
        '-dname', 'CN=Android Debug,O=Android,C=US',
        '-keyalg', 'RSA', '-keysize', '2048', '-validity', '10000'
    ) 'keytool'
}

# 8. sign
$signed = Join-Path $build 'b0agent.apk'
Run-Proc $java @(
    '-cp', $signerjar, 'com.android.apksigner.ApkSignerTool',
    'sign', '--ks', $ks,
    '--ks-pass', 'pass:android', '--key-pass', 'pass:android',
    '--ks-key-alias', 'androiddebugkey',
    '--out', $signed, $aligned
) 'apksigner'

Write-Host ""
Write-Host "BUILT OK -> $signed"
