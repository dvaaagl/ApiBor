# ApiBor — TokenHarbor Auto-Register Bot

Auto-register akun [TokenHarbor](https://tokenharbor.ai) + generate API key + test model `mimo-v2.5:free`.

## Cara Pakai

### 1. Clone & Install

```bash
git clone https://github.com/dvaaagl/ApiBor.git
cd ApiBor
pip install -r requirements.txt
```

### 2. Run

```bash
python bot.py
```

### 3. Dapatkan License

1. Jalankan `python bot.py`
2. Copy **Machine ID** yang muncul
3. Chat **@machine_id_bot** di Telegram
4. Kirim Machine ID kamu
5. Bot akan kasih **License Key** (trial 7 hari)
6. Paste key di bot.py

## Menu

```
[1] Buat 1 akun (+ test)
[2] Buat batch (N akun)
[3] Test semua API key
[4] List akun & key
[5] Test 1 key
[6] Inject ke 9router
[7] Lihat 9router entries
[0] Exit
```

## Command Line

```bash
python bot.py 1              # Buat 1 akun
python bot.py batch 10       # Buat 10 akun
python bot.py batch 10 --inject  # Batch + inject
python bot.py test           # Test semua key
python bot.py list           # List semua akun
python bot.py inject         # Inject ke 9router
```

## License

- **Trial**: 7 hari gratis
- **1 Machine ID = 1 Telegram user**
- License expires otomatis
- Chat **@machine_id_bot** untuk perpanjang

## Contact

- License: **@machine_id_bot** (Telegram)
- Issues: **@omopagll** (Telegram)

---

**Disclaimer:** Tool ini untuk pembelajaran. Penyalahgunaan bukan tanggung jawab pengembang.
