#!/usr/bin/env python3
"""
tools/audit_real_apps_compatibility.py
=============================================================================
SecretHandle — Empirical Compatibility Audit Tool for Real Android Apps
(Addressing MobiSys 2027 Reviewer Weakness W3 & Action Item MF-5)

Mục đích:
  Khảo sát và phân tích cấu trúc cây trợ năng (Accessibility Node Hierarchy) 
  của màn hình đăng nhập / nhập mã OTP trên 15–20 ứng dụng thực tế.
  Đánh giá khả năng tương thích của vị từ đích Match(d, x) và cơ chế Fallback Policy.

Cách sử dụng:
  1. Kết nối điện thoại thật (bật USB Debugging) hoặc khởi động Emulator:
     python tools/audit_real_apps_compatibility.py --list-devices
  2. Mở màn hình đăng nhập hoặc OTP của một ứng dụng trên điện thoại (vd: Vietcombank, MoMo, Shopee).
  3. Chạy lệnh chụp và phân tích màn hình hiện tại:
     python tools/audit_real_apps_compatibility.py --capture "Vietcombank" --category "Banking"
  4. Xuất báo cáo tổng kết và bảng LaTeX cho Phụ lục:
     python tools/audit_real_apps_compatibility.py --report
=============================================================================
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
import json
import subprocess
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

# Cấu hình đường dẫn ADB mặc định trên Windows
DEFAULT_ADB_PATHS = [
    r"C:\Users\ASUS\AppData\Local\Android\Sdk\platform-tools\adb.exe",
    "adb"
]

OUTPUT_DIR = Path("output")
DUMPS_DIR = Path("output/ui_dumps")
AUDIT_JSON_PATH = OUTPUT_DIR / "real_apps_compatibility_audit.json"


def find_adb():
    """Tìm đường dẫn adb khả dụng trên máy."""
    for path in DEFAULT_ADB_PATHS:
        try:
            res = subprocess.run([path, "version"], capture_output=True, text=True, check=False)
            if res.returncode == 0:
                return path
        except FileNotFoundError:
            continue
    return None


def run_adb(adb_cmd, args):
    """Chạy lệnh adb và trả về kết quả."""
    cmd = [adb_cmd] + args
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return res.returncode, res.stdout.strip(), res.stderr.strip()


def check_device(adb_cmd):
    """Kiểm tra thiết bị Android đang kết nối."""
    code, out, err = run_adb(adb_cmd, ["devices"])
    lines = [line.strip() for line in out.splitlines() if line.strip() and not line.startswith("List of devices")]
    devices = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            devices.append(parts[0])
    return devices


def get_device_info(adb_cmd, device_serial=None):
    """Lấy thông tin model thiết bị và phiên bản Android."""
    serial_args = ["-s", device_serial] if device_serial else []
    _, model, _ = run_adb(adb_cmd, serial_args + ["shell", "getprop", "ro.product.model"])
    _, release, _ = run_adb(adb_cmd, serial_args + ["shell", "getprop", "ro.build.version.release"])
    _, sdk, _ = run_adb(adb_cmd, serial_args + ["shell", "getprop", "ro.build.version.sdk"])
    return {
        "model": model.strip() or "unknown",
        "android_release": release.strip() or "unknown",
        "android_sdk": sdk.strip() or "unknown",
    }


def get_package_metadata(adb_cmd, package_name, device_serial=None):
    """Lấy versionName, versionCode, targetSdk của package trên thiết bị."""
    if not package_name or package_name == "unknown":
        return {"version_name": "unknown", "version_code": "unknown", "target_sdk": "unknown"}
    serial_args = ["-s", device_serial] if device_serial else []
    code, out, _ = run_adb(adb_cmd, serial_args + ["shell", "dumpsys", "package", package_name])
    version_name = "unknown"
    version_code = "unknown"
    target_sdk = "unknown"
    if code == 0 and out:
        for line in out.splitlines():
            s = line.strip()
            if version_code == "unknown" and s.startswith("versionCode="):
                for token in s.split():
                    if token.startswith("versionCode="):
                        version_code = token.split("=", 1)[1]
                    elif token.startswith("targetSdk="):
                        target_sdk = token.split("=", 1)[1]
            elif version_name == "unknown" and s.startswith("versionName="):
                version_name = s.split("=", 1)[1].strip()
            if version_code != "unknown" and version_name != "unknown":
                break
    return {
        "version_name": version_name,
        "version_code": version_code,
        "target_sdk": target_sdk,
    }


def capture_hierarchy(adb_cmd, device_serial=None):
    """Chụp window_dump.xml từ thiết bị qua ADB (chỉ giữ metadata UI tĩnh, xóa dump tạm ngay)."""
    serial_args = ["-s", device_serial] if device_serial else []

    # 1. Lấy thông tin foreground package & activity trước
    code, pkg_out, _ = run_adb(adb_cmd, serial_args + ["shell", "dumpsys", "window", "displays"])
    foreground_pkg = "unknown"
    for line in pkg_out.splitlines():
        if "mCurrentFocus" in line or "mFocusedApp" in line:
            for p in line.split():
                if "/" in p and not p.startswith("/") and "." in p.split("/")[0]:
                    foreground_pkg = p.split("/")[0].strip("{}")
                    break
            if foreground_pkg != "unknown":
                break

    # 2. Chạy uiautomator dump trên thiết bị
    code, out, err = run_adb(adb_cmd, serial_args + ["shell", "uiautomator", "dump", "/sdcard/window_dump.xml"])
    if code != 0 or "dumped to:" not in out.lower():
        code, out, err = run_adb(adb_cmd, serial_args + ["shell", "uiautomator", "dump", "--compressed", "/sdcard/window_dump.xml"])
        if code != 0 or "dumped to:" not in out.lower():
            print(f"[!] Cảnh báo: uiautomator dump bị chặn hoặc rỗng ({err or out}); ghi nhận fallback.")
            return foreground_pkg, ""

    # 3. Kéo file xml về máy host, đọc vào RAM rồi xóa file tạm ngay để không lưu dữ liệu nhạy cảm
    DUMPS_DIR.mkdir(parents=True, exist_ok=True)
    temp_local_xml = DUMPS_DIR / "temp_dump.xml"
    code, out, err = run_adb(adb_cmd, serial_args + ["pull", "/sdcard/window_dump.xml", str(temp_local_xml)])
    run_adb(adb_cmd, serial_args + ["shell", "rm", "-f", "/sdcard/window_dump.xml"])
    if code != 0 or not temp_local_xml.exists():
        print(f"[!] Không thể đọc XML dump ({err or out}); ghi nhận fallback.")
        return foreground_pkg, ""

    content = temp_local_xml.read_text(encoding="utf-8", errors="replace")
    try:
        temp_local_xml.unlink()
    except OSError:
        pass
    return foreground_pkg, content


def parse_ui_hierarchy(xml_content):
    """Phân tích các node nhập liệu tĩnh trong XML (không lưu text người dùng)."""
    if not xml_content.strip():
        return []
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        print(f"[-] Lỗi parse XML: {e}")
        return []

    input_nodes = []

    for node in root.iter("node"):
        cls = node.attrib.get("class", "")
        res_id = node.attrib.get("resource-id", "")
        text = node.attrib.get("text", "")
        desc = node.attrib.get("content-desc", "")
        hint_attr = node.attrib.get("hint", "")
        is_password = node.attrib.get("password", "false").lower() == "true"
        focusable = node.attrib.get("focusable", "false").lower() == "true"
        bounds = node.attrib.get("bounds", "")

        lower_cls = cls.lower()
        is_edit_text = "edittext" in lower_cls or "autocompletetextview" in lower_cls
        is_webview = "webview" in lower_cls
        is_custom_input = (
            is_webview
            or "flutter" in lower_cls
            or "react" in lower_cls
            or "canvas" in lower_cls
            or "surfaceview" in lower_cls
            or "composeview" in lower_cls
            or any(k in res_id.lower() for k in ("pin", "otp", "code", "digit", "numpad", "keypad"))
        )

        # Kiểm tra gợi ý trường từ resource-id, content-desc, hint, placeholder text (không ghi text ra đĩa)
        hints = []
        combined = " ".join([res_id.lower(), desc.lower(), hint_attr.lower(), text.lower()])

        if any(k in combined for k in ("otp", "mã xác thực", "mã otp", "verification", "verify_code", "pin", "2fa", "mã kích hoạt", "passcode")):
            hints.append("smsOTPCode")
        if any(k in combined for k in ("pass", "mật khẩu", "pwd")) or is_password:
            hints.append("password")
        if any(k in combined for k in ("phone", "số điện thoại", "sdt", "mobile", "msisdn")):
            hints.append("phone")
        if any(k in combined for k in ("user", "account", "email", "tài khoản", "đăng nhập")):
            hints.append("username")

        if is_edit_text or (focusable and is_custom_input) or is_webview:
            if is_edit_text and ("smsOTPCode" in hints or "password" in hints):
                compat_status = "DIRECT_MATCH"
                reason = "Standard EditText with explicit OTP/password semantic signal"
            elif is_edit_text:
                compat_status = "NUMERIC_STANDARD"
                reason = "Standard EditText without explicit OTP/password hint (package+class fallback)"
            else:
                compat_status = "CUSTOM_CANVAS_FALLBACK"
                reason = "WebView / custom / opaque view container (package boundary + touch confirmation)"

            input_nodes.append({
                "class": cls,
                "resource_id": res_id,
                "content_desc": desc,
                "is_password": is_password,
                "detected_hints": hints,
                "bounds": bounds,
                "compatibility_tier": compat_status,
                "reason": reason
            })

    return input_nodes


def _pick_representative_class(fields):
    """Chọn class đại diện theo mức ưu tiên tương thích cao nhất."""
    if not fields:
        return "CustomView/Opaque"
    for tier in ("DIRECT_MATCH", "NUMERIC_STANDARD", "CUSTOM_CANVAS_FALLBACK"):
        for node in fields:
            if node.get("compatibility_tier") == tier:
                return node["class"].split(".")[-1]
    return fields[0]["class"].split(".")[-1]


def record_audit(app_name, category, foreground_pkg, nodes, pkg_meta=None, device_info=None, xml_ok=True):
    """Ghi nhận kết quả khảo sát của 1 ứng dụng vào file JSON."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pkg_meta = pkg_meta or {}

    data = {"timestamp": datetime.now().isoformat(), "device": device_info or {}, "audited_apps": []}
    if AUDIT_JSON_PATH.exists():
        try:
            with open(AUDIT_JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            pass

    if device_info:
        data["device"] = device_info
    data["timestamp"] = datetime.now().isoformat()

    # Xóa bản ghi cũ của app này nếu có để ghi đè
    data["audited_apps"] = [a for a in data.get("audited_apps", []) if a.get("app_name") != app_name]

    has_direct = any(n["compatibility_tier"] == "DIRECT_MATCH" for n in nodes)
    has_numeric = any(n["compatibility_tier"] == "NUMERIC_STANDARD" for n in nodes)

    if has_direct:
        overall_status = "DIRECT_COMPATIBLE"
    elif has_numeric:
        overall_status = "STANDARD_INPUT_FALLBACK"
    else:
        overall_status = "CUSTOM_VIEW_FALLBACK"

    record = {
        "app_name": app_name,
        "category": category,
        "package_name": foreground_pkg,
        "version_name": pkg_meta.get("version_name", "unknown"),
        "version_code": pkg_meta.get("version_code", "unknown"),
        "target_sdk": pkg_meta.get("target_sdk", "unknown"),
        "ui_dump_status": "ok" if xml_ok else "blocked_or_empty",
        "audited_at": datetime.now().isoformat(),
        "input_field_count": len(nodes),
        "primary_status": overall_status,
        "fields": nodes
    }

    data["audited_apps"].append(record)

    with open(AUDIT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[+] Đã ghi nhận '{app_name}' ({foreground_pkg} v{record['version_name']} / {record['version_code']}) -> {overall_status}")
    print(f"    Tổng số node nhập liệu phát hiện: {len(nodes)}")


def generate_report():
    """Tạo bảng báo cáo tóm tắt Markdown và LaTeX cho Phụ lục."""
    if not AUDIT_JSON_PATH.exists():
        print(f"[-] Chưa có dữ liệu tại {AUDIT_JSON_PATH}. Hãy chạy --capture trước.")
        return

    with open(AUDIT_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    apps = data.get("audited_apps", [])
    if not apps:
        print("[-] Danh sách ứng dụng trống.")
        return

    dev = data.get("device", {})
    total = len(apps)
    direct_count = sum(1 for a in apps if a["primary_status"] == "DIRECT_COMPATIBLE")
    numeric_count = sum(1 for a in apps if a["primary_status"] == "STANDARD_INPUT_FALLBACK")
    custom_count = sum(1 for a in apps if a["primary_status"] == "CUSTOM_VIEW_FALLBACK")

    print("\n" + "="*75)
    print(f" REAL APPS COMPATIBILITY AUDIT ({dev.get('model', 'Android')} / Android {dev.get('android_release', '?')} API {dev.get('android_sdk', '?')})")
    print("="*75)
    print(f"Tổng số ứng dụng đã khảo sát: {total}")
    print(f" - Direct Match (EditText + OTP/Password signal):      {direct_count}/{total} ({direct_count/total*100:.1f}%)")
    print(f" - Standard Input Fallback (Standard EditText):        {numeric_count}/{total} ({numeric_count/total*100:.1f}%)")
    print(f" - Custom View / Opaque Fallback (Touch Confirm):      {custom_count}/{total} ({custom_count/total*100:.1f}%)")
    print("-"*75)

    print(f"\n| # | App | Category | Package | Version | UI Class | Status |")
    print(f"|---|---|---|---|---|---|---|")
    for i, a in enumerate(apps, 1):
        cls_name = _pick_representative_class(a.get("fields", []))
        ver = a.get("version_name", "?")
        print(f"| {i} | {a['app_name']} | {a['category']} | `{a['package_name']}` | `{ver}` | `{cls_name}` | **{a['primary_status']}** |")

    tex_path = OUTPUT_DIR / "real_apps_compatibility_table.tex"
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write("% Auto-generated by tools/audit_real_apps_compatibility.py\n")
        f.write("\\begin{table*}[t]\n\\centering\\footnotesize\n")
        f.write("\\caption{Empirical compatibility audit of \\SH{} destination matching across real Google Play applications captured on a physical Samsung Galaxy A52s (Android 14, API 34). Direct: standard \\texttt{EditText} with explicit OTP/password semantic attributes; Standard Fallback: standard \\texttt{EditText} matched by package+class; Custom/Opaque Fallback: custom view, WebView, or protected window handled via foreground-package boundary plus single-tap confirmation.}\n")
        f.write("\\label{tab:app_compatibility}\n")
        f.write("\\begin{tabular*}{\\textwidth}{@{\\extracolsep{\\fill}}llllllc@{}}\n\\toprule\n")
        f.write("Application & Category & Package Identifier & Version & Input Class & Matching & Fallback \\\\\n\\midrule\n")
        for a in apps:
            cls_name = _pick_representative_class(a.get("fields", [])).replace("_", "\\_")
            ver = str(a.get("version_name", "?")).split()[0][:18].replace("_", "\\_")
            pkg_tex = a["package_name"].replace("_", "\\_")
            app_tex = a["app_name"].replace("&", "\\&")
            cat_tex = a["category"].replace("&", "\\&")
            if a["primary_status"] == "DIRECT_COMPATIBLE":
                matching = "Direct"
                fallback = "None"
            elif a["primary_status"] == "STANDARD_INPUT_FALLBACK":
                matching = "Package+Class"
                fallback = "Touch Confirm"
            else:
                matching = "Package-only"
                fallback = "Touch Confirm"
            f.write(f"{app_tex} & {cat_tex} & \\texttt{{{pkg_tex}}} & \\texttt{{{ver}}} & \\texttt{{{cls_name}}} & {matching} & {fallback} \\\\\n")
        f.write("\\bottomrule\n\\end{tabular*}\n\\end{table*}\n")

    print(f"\n[+] Đã xuất mã bảng LaTeX tại: {tex_path}")


def main():
    parser = argparse.ArgumentParser(description="SecretHandle Real Apps Compatibility Audit Tool")
    parser.add_argument("--list-devices", action="store_true", help="Liệt kê thiết bị Android đang kết nối")
    parser.add_argument("--capture", type=str, help="Chụp màn hình hiện tại và đặt tên ứng dụng (vd: 'Vietcombank')")
    parser.add_argument("--category", type=str, default="Finance", help="Phân loại ứng dụng (vd: Finance, E-Commerce, Auth)")
    parser.add_argument("--report", action="store_true", help="Xuất báo cáo tổng kết và bảng LaTeX cho Phụ lục")
    args = parser.parse_args()

    adb_cmd = find_adb()
    if not adb_cmd:
        print("[-] Không tìm thấy adb.exe! Vui lòng cài Android SDK hoặc thêm adb vào PATH.")
        sys.exit(1)

    if args.list_devices:
        devices = check_device(adb_cmd)
        if devices:
            print(f"[+] Các thiết bị đang kết nối: {', '.join(devices)}")
        else:
            print("[-] Chưa có thiết bị nào kết nối qua ADB.")
            print("    Hãy cắm cáp USB (bật USB Debugging) hoặc chạy Android Emulator.")
        return

    if args.capture:
        devices = check_device(adb_cmd)
        if not devices:
            print("[-] Lỗi: Không tìm thấy thiết bị Android nào kết nối qua ADB để chụp màn hình!")
            print("    Vui lòng kiểm tra lại cáp kết nối hoặc khởi động trình giả lập.")
            sys.exit(1)

        print(f"[*] Đang chụp cây giao diện từ thiết bị {devices[0]}...")
        res = capture_hierarchy(adb_cmd, devices[0])
        if not res:
            sys.exit(1)

        pkg, xml_content = res
        print(f"[*] Đang nhận diện foreground package: {pkg}")
        device_info = get_device_info(adb_cmd, devices[0])
        pkg_meta = get_package_metadata(adb_cmd, pkg, devices[0])
        nodes = parse_ui_hierarchy(xml_content)
        record_audit(
            args.capture,
            args.category,
            pkg,
            nodes,
            pkg_meta=pkg_meta,
            device_info=device_info,
            xml_ok=bool(xml_content.strip()),
        )
        return

    if args.report:
        generate_report()
        return

    parser.print_help()


if __name__ == "__main__":
    main()

