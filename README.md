# ApiBor — TokenHarbor Auto-Register Bot

Auto-register akun [TokenHarbor](https://tokenharbor.ai) + generate API key + test model `mimo-v2.5:free`.

## Fitur

- Auto-register akun via temp email (mail.tm)
- Verifikasi email otomatis (IMAP polling)
- Buat API key + accept free model consent
- Test model `mimo-v2.5:free`
- Batch register (N akun sekaligus)
- Inject ke 9router (optional)
- License-protected (machine ID binding)

## Instalasi

```bash
git clone https://github.com/dvaaagl/ApiBor.git
cd ApiBor
pip install -r requirements.txt
```

## Cara Pakai

```bash
python bot.py
```

### Menu

```
[1] Buat 1 akun (+ test + inject)
[2] Buat batch (N akun)
[3] Test semua API key
[4] List akun & key
[5] Test 1 key (input)
[6] Inject semua ke 9router
[7] Lihat 9router entries
[0] Exit
```

### Command Line

```bash
python bot.py 1              # Buat 1 akun
python bot.py batch 10       # Buat 10 akun
python bot.py batch 10 --inject  # Batch + inject ke 9router
python bot.py test           # Test semua key
python bot.py list           # List semua akun
python bot.py inject         # Inject semua ke 9router
python bot.py 9router        # Lihat 9router entries
```

## License

Bot ini **license-protected**. Setiap akun terikat ke Machine ID.

### Mendapatkan License

1. Jalankan `python bot.py`
2. Copy **Machine ID** yang muncul
3. Chat **@omopagll** di Telegram
4. Kirim Machine ID, tunggu license key
5. Paste license key saat diminta

### Apa itu Machine ID?

Machine ID adalah identifikasi unik perangkat Anda (gabungan hostname + serial number). License key di-generate khusus untuk Machine ID Anda — tidak bisa dipakai di perangkat lain.

## File Structure

```
ApiBor/
├── bot.py              # Bot utama (encoded, jalankan ini)
├── _core.py            # Core logic (TokenHarbor API interaction)
├── bot_license_src.py  # License system source (reference)
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
└── README.md           # This file
```

## Environment

Copy `.env.example` ke `.env` dan isi:

```env
# Proxy (optional, recommended untuk batch besar)
PROXY=http://user:pass@proxy:port
```

## Notes

- Gunakan proxy untuk menghindari rate limit
- Batch besar (50+) butuh waktu 15-30 menit
- Email verification otomatis via mail.tm
- API key tersimpan di `apikeys.txt`
- Akun tersimpan di `accounts.json`

## Contact

- Telegram: **@omopagll**
- License issues: DM dengan Machine ID

---

**Disclaimer:** Tool ini untuk pembelajaran dan penggunaan pribadi. Penyalahgunaan untuk aktivitas ilegal bukan tanggung jawab pengembang.
