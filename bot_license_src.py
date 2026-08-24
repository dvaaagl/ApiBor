#!/usr/bin/env python3
"""
botbor — TokenHarbor Auto-Register Bot (License-Protected)
Contact @omopagll on Telegram to get your license key.
"""
import sys, os, base64, hashlib, hmac, platform, subprocess

# ─── License System ─────────────────────────────────────────────
LICENSE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".license")
_SECRET = "lxbW2govL6wRGVtJfK3fe55M00Er49"

def _machine_id():
    import platform
    raw = f"{platform.node()}-{platform.machine()}-{platform.processor()}"
    for p in ["/sys/class/dmi/id/product_uuid", "/sys/class/dmi/id/board_serial"]:
        try:
            with open(p) as f: raw += f.read().strip()
        except: pass
    return hashlib.sha256(raw.encode()).hexdigest()[:16].upper()

def _gen_key(mid):
    return hmac.new(_SECRET.encode(), mid.encode(), hashlib.sha256).hexdigest()[:32].upper()

def _verify(mid, key):
    clean = key.replace('-', '').replace(' ', '').upper()
    return hmac.compare_digest(_gen_key(mid), clean)

def _load_license():
    if os.path.exists(LICENSE_FILE):
        with open(LICENSE_FILE) as f: return f.read().strip()
    return None

def _save_license(key):
    with open(LICENSE_FILE, "w") as f: f.write(key)

def _check_license():
    mid = _machine_id()
    key = _load_license()
    if key and _verify(mid, key): return True
    print(f"""
  LICENSE REQUIRED
  ═══════════════════════════════════
  Your Machine ID: {mid}

  Send this ID to @omopagll on Telegram
  to get your license key.
  ═══════════════════════════════════
""")
    entered = input("  License key: ").strip()
    if not entered: print("  No key. Bye."); return False
    if _verify(mid, entered):
        _save_license(entered)
        print("  License activated!")
        return True
    print("  Invalid key. Contact @omopagll"); return False

if not _check_license():
    sys.exit(1)

# ─── Load bot core ─────────────────────────────────────────────
_core = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_core.py")
exec(compile(open(_core).read(), _core, 'exec'))
main()
