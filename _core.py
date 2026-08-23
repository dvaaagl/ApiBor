#!/usr/bin/env python3
"""_core.py — botbor core (will be encoded)"""
import requests, re, json, random, string, uuid, urllib.parse, time, sys, os, sqlite3
from datetime import datetime, timezone

BASE = "https://tokenharbor.ai"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"
ACTION_ID = "6003703e71fc5dc99543154237e9a9267997419301"
ACTION_KEY = "kb59e6b88b9f36883e58e38e7e48870c6"
NEXT_ACTION = "607ec2c1a962aa81ad67a2483c54b0cfadfda875b2"
ROUTER = urllib.parse.quote('["",{"children":["login",{"children":["__PAGE__",{},null,null,0]},null,null,0]},null,null,20]')
DIR = os.path.dirname(os.path.abspath(__file__))
APIKEY_FILE = os.path.join(DIR, "apikeys.txt")
ACCOUNT_FILE = os.path.join(DIR, "accounts.json")
TEST_MODEL = "mimo-v2.5:free"
NINE_ROUTER_DB = os.path.expanduser("~/.9router/db/data.sqlite")
PROXY = os.environ.get("BOTBOR_PROXY", "")
if not PROXY:
    env_file = os.path.join(DIR, ".env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if line.strip().startswith("BOTBOR_PROXY="):
                    PROXY = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
P = {"http": PROXY, "https": PROXY} if PROXY else {}

def rand_pwd():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12)) + '!Aa1'

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"  [{ts}] [{level}] {msg}")

def make_signup_body(email, pwd):
    fp = str(uuid.uuid4())
    bd = "----WebKitFormBoundary" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    parts = []
    def af(n, v=""):
        parts.append(f'--{bd}\r\nContent-Disposition: form-data; name="{n}"\r\n\r\n{v}')
    af("1_$ACTION_REF_1")
    af("1_$ACTION_1:0", json.dumps({"id": ACTION_ID, "bound": "$@1"}))
    af("1_$ACTION_1:1", '["$undefined"]')
    af("1_$ACTION_KEY", ACTION_KEY)
    af("1_device_fingerprint", fp); af("1_timezone"); af("1_next")
    af("1_email", email); af("1_password", pwd); af("1_invite_code")
    af("0", '["$undefined","$K1"]')
    body = "\r\n".join(parts) + f"\r\n--{bd}--\r\n"
    headers = {
        "Content-Type": f"multipart/form-data; boundary={bd}",
        "Accept": "text/x-component",
        "Next-Action": NEXT_ACTION,
        "Next-Router-State-Tree": ROUTER,
        "Origin": BASE, "Referer": f"{BASE}/login",
    }
    return body, headers

def load_accounts():
    if os.path.exists(ACCOUNT_FILE):
        with open(ACCOUNT_FILE) as f: return json.load(f)
    return []

def save_accounts(data):
    with open(ACCOUNT_FILE, "w") as f: json.dump(data, f, indent=2)

def load_keys():
    if os.path.exists(APIKEY_FILE):
        with open(APIKEY_FILE) as f: return [l.strip() for l in f if l.strip()]
    return []

def save_key(key):
    with open(APIKEY_FILE, "a") as f: f.write(f"{key}\n")

def inject_to_9router(api_key, email, user_id=""):
    try:
        conn = sqlite3.connect(NINE_ROUTER_DB); cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM providerConnections WHERE provider='tokenbor'")
        count = cur.fetchone()[0]
        conn_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        label = f"{email.split('@')[0][:6]} #{count + 1}"
        data = json.dumps({"defaultModel": "mimo-v2.5:free", "apiKey": api_key, "testStatus": "active",
            "providerSpecificData": {"prefix": "tokenbor", "apiType": "chat", "baseUrl": "https://tokenharbor.ai/v1", "nodeName": "tokenbor"}})
        cur.execute("INSERT INTO providerConnections (id, provider, authType, name, email, priority, isActive, data, createdAt, updatedAt) VALUES (?, 'tokenbor', 'api_key', ?, ?, 0, 1, ?, ?, ?)",
            (conn_id, label, email, data, now, now))
        conn.commit(); conn.close()
        return True, label
    except Exception as e: return False, str(e)[:60]

def inject_show_9router():
    try:
        conn = sqlite3.connect(NINE_ROUTER_DB); cur = conn.cursor()
        cur.execute("SELECT id, name, email, isActive FROM providerConnections WHERE provider='tokenbor'")
        rows = cur.fetchall(); conn.close(); return rows
    except: return []

def test_free_model(api_key):
    try:
        r = requests.post(f"{BASE}/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            timeout=30, json={"model": TEST_MODEL, "messages": [{"role": "user", "content": "say ok"}], "max_tokens": 20})
        if r.status_code == 200:
            reply = r.json().get("choices", [{}])[0].get("message", {}).get("content", "")
            return True, f"200 OK - {reply[:30]}"
        else: return False, f"{r.status_code} - {r.text[:60]}"
    except Exception as e: return False, f"ERR - {str(e)[:50]}"

def register_one():
    log("Creating temp email...")
    email_r = requests.post("https://api.tempmail.lol/v2/inbox/create", timeout=10)
    email = email_r.json()["address"]
    email_token = email_r.json()["token"]
    pwd = rand_pwd()
    log(f"Email: {email}")
    s = requests.Session(); s.headers.update({"User-Agent": UA})
    log("Loading login page...")
    for attempt in range(5):
        try: s.get(f"{BASE}/login", proxies=P or None, timeout=20); break
        except: log(f"  Retry {attempt+1}/5...", "WARN"); time.sleep(3)
    log("Submitting signup...")
    body, headers = make_signup_body(email, pwd)
    for attempt in range(5):
        try: r = s.post(f"{BASE}/login", data=body, headers=headers, proxies=P or None, timeout=25); break
        except: log(f"  Retry {attempt+1}/5...", "WARN"); time.sleep(3)
    else: return None, "proxy failed after 5 retries"
    if "signedIn" not in r.text:
        errors = re.findall(r'"error":"([^"]+)"', r.text)
        err = errors[0] if errors else f"HTTP {r.status_code}"
        log(f"Signup FAILED: {err}", "ERROR"); return None, err
    uid = re.findall(r'"userId":\s*"([^"]+)"', r.text)
    log(f"Signup OK - userId: {uid[0] if uid else '?'}")
    log("Cleaning auto-created keys...")
    r2 = s.get(f"{BASE}/api/keys", headers={"Accept": "application/json"}, proxies=P or None, timeout=15)
    for k in r2.json().get("keys", []):
        s.delete(f"{BASE}/api/keys/{k['id']}", proxies=P or None, timeout=10)
    log("Creating API key...")
    r3 = s.post(f"{BASE}/api/keys", json={"label": f"botbor-{random.randint(100,999)}"},
        headers={"Accept": "application/json", "Content-Type": "application/json"}, proxies=P or None, timeout=15)
    if r3.status_code != 201: log(f"Key create FAILED: {r3.status_code}", "ERROR"); return None, f"key create failed {r3.status_code}"
    key = r3.json().get("plaintext")
    if not key: log("No plaintext in response", "ERROR"); return None, "no plaintext"
    log(f"Key created: {key[:35]}...")
    log("Accepting free model consent...")
    rc = s.post(f"{BASE}/api/me/privacy", json={"free_models_enabled": True},
        headers={"Accept": "application/json", "Content-Type": "application/json"}, proxies=P or None, timeout=10)
    consent_ok = rc.status_code == 200 and '"ok":true' in rc.text
    log(f"Consent: {'Y' if consent_ok else 'N'} ({rc.status_code})")
    log("Waiting for verification email (max 90s)...")
    verified = verify_email(email_token)
    log(f"Email {'verified' if verified else 'NOT verified (timeout)'}")
    return {"email": email, "password": pwd, "userId": uid[0] if uid else "", "api_key": key, "email_token": email_token, "verified": verified, "consent": consent_ok}, None

def verify_email(email_token, max_wait=90):
    start = time.time()
    while time.time() - start < max_wait:
        try:
            r = requests.get(f"https://api.tempmail.lol/v2/inbox?token={email_token}", timeout=10)
            for em in r.json().get("emails", []):
                links = re.findall(r'(https://tokenharbor\.ai/verify-email\?[^\s"<>]+)', em.get("body", ""))
                if links: requests.get(links[0], timeout=15, allow_redirects=True); return True
        except: pass
        time.sleep(8)
    return False

def run_batch(n, inject=False):
    success = 0
    for i in range(n):
        print(f"\n  [{i+1}/{n}] " + "="*40)
        for attempt in range(5):
            try:
                account, err = register_one()
                if account:
                    accounts = load_accounts(); accounts.append(account); save_accounts(accounts); save_key(account["api_key"]); success += 1
                    log("Testing free model...")
                    ok, info = test_free_model(account["api_key"])
                    log(f"Test {TEST_MODEL}: {'OK' if ok else 'FAIL'} {info}")
                    account["test_result"] = info
                    v = "Y" if account.get("verified") else "N"; c = "Y" if account.get("consent") else "N"; t = "Y" if ok else "N"
                    print(f"  RESULT: {account['email']} [verify:{v}] [consent:{c}] [model:{t}]")
                    if inject:
                        injected, msg = inject_to_9router(account["api_key"], account["email"], account.get("userId", ""))
                        log(f"{'Injected' if injected else 'Inject failed'}: {msg}")
                    save_accounts(accounts); break
                else: log(f"Attempt {attempt+1}: {err[:40]}", "ERROR")
            except Exception as e: log(f"Attempt {attempt+1}: {str(e)[:30]}", "ERROR")
            time.sleep(random.randint(3, 7))
        if i < n - 1: wait = random.randint(8, 15); log(f"Waiting {wait}s..."); time.sleep(wait)
    return success

def cmd_create_one(inject=True):
    print(f"\n{'='*50}\n  Register 1 akun + test {TEST_MODEL}\n{'='*50}")
    account, err = register_one()
    if not account: print(f"\n  FAILED: {err}"); return
    accounts = load_accounts(); accounts.append(account); save_accounts(accounts); save_key(account["api_key"])
    print(); log(f"Testing {TEST_MODEL}...")
    ok, info = test_free_model(account["api_key"])
    log(f"Test: {'OK' if ok else 'FAIL'} {info}")
    v = "Y" if account.get("verified") else "N"; t = "Y" if ok else "N"
    print(f"\n  Email:    {account['email']}")
    print(f"  Password: {account['password']}")
    print(f"  Key:      {account['api_key'][:35]}...")
    print(f"  Verify:   {v} | Model: {t}")
    if inject:
        ans = input("\n  Inject ke 9router? (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            injected, msg = inject_to_9router(account["api_key"], account["email"], account.get("userId", ""))
            print(f"  {'OK' if injected else 'FAIL'}: {msg}")

def cmd_test_all():
    keys = load_keys()
    if not keys: print("\n  No keys in apikeys.txt"); return
    print(f"\n  Testing {len(keys)} keys..."); ok = 0
    for i, k in enumerate(keys):
        valid, info = test_free_model(k)
        print(f"  {'OK' if valid else 'FAIL'} [{i+1}] {k[:35]}... -> {info}")
        if valid: ok += 1
    print(f"\n  {ok}/{len(keys)} valid")

def cmd_test_one():
    key = input("\n  Masukkan key: ").strip()
    if not key: print("  Empty"); return
    valid, info = test_free_model(key)
    print(f"  {'OK' if valid else 'FAIL'} {info}")

def cmd_inject_all():
    accounts = load_accounts()
    if not accounts: print("\n  No accounts"); return
    print(f"\n  Inject {len(accounts)} accounts..."); ok = 0
    for a in accounts:
        injected, msg = inject_to_9router(a["api_key"], a["email"], a.get("userId", ""))
        if injected: ok += 1
        print(f"  {'OK' if injected else 'FAIL'} {a['email']} -> {msg}")
    print(f"\n  {ok}/{len(accounts)} injected")

def cmd_list():
    accts = load_accounts(); keys = load_keys()
    print(f"\n  Accounts: {len(accts)} | Keys: {len(keys)}")
    for i, a in enumerate(accts):
        print(f"  [{i+1}] {a['email']} | {a.get('api_key','?')[:35]}...")

def cmd_9router_list():
    rows = inject_show_9router()
    print(f"\n  9router tokenbor entries: {len(rows)}")
    for r in rows: print(f"  {r[0][:8]} | {r[1]} | {r[2]} | active={r[3]}")

def menu():
    print(f"""
  botbor - TokenHarbor Auto-Register
  Model: {TEST_MODEL}

  [1] Buat 1 akun (+ test + inject)
  [2] Buat batch (N akun)
  [3] Test semua API key
  [4] List akun & key
  [5] Test 1 key (input)
  [6] Inject semua ke 9router
  [7] Lihat 9router entries
  [0] Exit""")

def main():
    args = sys.argv[1:]
    if not args:
        while True:
            menu()
            choice = input("  Pilih: ").strip()
            if choice == "1": cmd_create_one()
            elif choice == "2":
                n = input("  Jumlah: ").strip()
                inj = input("  Inject? (y/n): ").strip().lower()
                if n.isdigit() and int(n) > 0:
                    ok = run_batch(int(n), inject=inj in ("y", "yes"))
                    print(f"\n  Done: {ok}/{int(n)}")
            elif choice == "3": cmd_test_all()
            elif choice == "4": cmd_list()
            elif choice == "5": cmd_test_one()
            elif choice == "6": cmd_inject_all()
            elif choice == "7": cmd_9router_list()
            elif choice == "0": print("  Bye!"); break
    elif args[0] == "1": cmd_create_one("--no-inject" not in args)
    elif args[0] == "batch":
        n = int(args[1]) if len(args) > 1 else 5
        inject = "--inject" in args
        ok = run_batch(n, inject=inject)
        print(f"\n  Done: {ok}/{n}")
    elif args[0] == "test": cmd_test_all()
    elif args[0] == "list": cmd_list()
    elif args[0] == "inject": cmd_inject_all()
    elif args[0] == "9router": cmd_9router_list()
    else: print(f"Usage: {sys.argv[0]} [1|batch N [--inject]|test|list|inject|9router]")

if __name__ == "__main__": main()
