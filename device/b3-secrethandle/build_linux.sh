#!/usr/bin/env bash
# Gradle-free CLI build for the B3 prototype (aapt2 + javac + d8 + zipalign + apksigner).
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
SDK=${ANDROID_HOME:-$HOME/android-sdk}
BT=$SDK/build-tools/35.0.0
ANDROID_JAR=$SDK/platforms/android-34/android.jar
BUILD=$ROOT/build

echo "== 0. toolchain =="
java -version 2>&1 | head -1
javac -version
ls -d "$BT" "$ANDROID_JAR"

rm -rf "$BUILD"
mkdir -p "$BUILD/classes" "$BUILD/dex"

echo "== 1. aapt2 compile + link =="
"$BT/aapt2" compile --dir "$ROOT/android/res" -o "$BUILD/res.zip"
"$BT/aapt2" link -o "$BUILD/base.apk" -I "$ANDROID_JAR" \
  --manifest "$ROOT/android/AndroidManifest.xml" \
  "$BUILD/res.zip" \
  --min-sdk-version 24 --target-sdk-version 34 \
  --version-code 1 --version-name 0.1

echo "== 2. javac =="
mapfile -t SRC < <(find "$ROOT/android/src" -name '*.java')
javac -source 8 -target 8 -encoding UTF-8 -nowarn \
  -bootclasspath "$ANDROID_JAR" -d "$BUILD/classes" "${SRC[@]}"

echo "== 3. jar =="
(cd "$BUILD/classes" && jar cf "$BUILD/classes.jar" .)

echo "== 4. d8 =="
java -cp "$BT/lib/d8.jar" com.android.tools.r8.D8 \
  --min-api 24 --lib "$ANDROID_JAR" --output "$BUILD/dex" "$BUILD/classes.jar"

echo "== 5. add classes.dex (pinned timestamp) =="
python3 - "$BUILD/base.apk" "$BUILD/dex/classes.dex" <<'PY'
import os
import sys
import zipfile

apk, dex = sys.argv[1], sys.argv[2]
tmp = apk + ".tmp"
with zipfile.ZipFile(apk) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        if item.filename == "classes.dex":
            continue
        zout.writestr(item, zin.read(item.filename))
    zi = zipfile.ZipInfo("classes.dex", date_time=(1980, 1, 1, 0, 0, 0))
    zi.compress_type = zipfile.ZIP_DEFLATED
    zi.external_attr = 0o644 << 16
    with open(dex, "rb") as fh:
        zout.writestr(zi, fh.read())
os.replace(tmp, apk)
print("classes.dex added")
PY

echo "== 6. zipalign =="
"$BT/zipalign" -f -p 4 "$BUILD/base.apk" "$BUILD/aligned.apk"

echo "== 7. sign =="
"$BT/apksigner" sign --ks "$ROOT/debug.keystore" \
  --ks-pass pass:android --key-pass pass:android \
  --ks-key-alias androiddebugkey \
  --out "$BUILD/b3secrethandle.apk" "$BUILD/aligned.apk"
"$BT/apksigner" verify "$BUILD/b3secrethandle.apk"

echo "BUILT OK -> $BUILD/b3secrethandle.apk"
sha256sum "$BUILD/b3secrethandle.apk"
