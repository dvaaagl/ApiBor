# botbor — TokenHarbor Auto-Register Bot

Automated TokenHarbor account registration, free model activation, and 9router injection.

## Features
- Auto-register via temp email
- Free model consent (`mimo-v2.5:free`)
- API key creation + testing
- 9router SQLite injection
- Batch mode (N accounts)

## Setup
```bash
git clone https://github.com/dvaaagl/ApiBor.git
cd botbor
pip install -r requirements.txt
```
a
## License Required
This bot is license-protected. On first run, you'll see your **Machine ID**.

**To get a license key:**
1. Run the bot: `python3 bot.py`
2. Copy your **Machine ID** shown on screen
3. Send it to **[@omopagll](https://t.me/omopagll)** on Telegram
4. Paste the license key when prompted

## Usage
```bash
python3 bot.py                    # Interactive menu
python3 bot.py 1                  # Register 1 account
python3 bot.py 1 --no-inject      # Register without 9router inject
python3 bot.py batch 5            # Register 5 accounts
python3 bot.py batch 5 --inject   # Register 5 + inject to 9router
python3 bot.py test               # Test all API keys
python3 bot.py list               # List accounts & keys
python3 bot.py inject             # Inject all to 9router
python3 bot.py 9router            # Show 9router entries
```

## Proxy (Optional)
```bash
export BOTBOR_PROXY="http://user:pass@proxy:port"
# or add to .env file
```

## License
Proprietary. Contact [@omopagll](https://t.me/omopagll) for license.
