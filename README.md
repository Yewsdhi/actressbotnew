# Actress Arena Gold 🎬

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://www.heroku.com/deploy?template=https://github.com/Yewsdhi/actressbotnew)

> **Before using the button:** upload this project to a public GitHub repository named `Actress-Arena-Gold`, then replace `YOUR_GITHUB_USERNAME` in this README with your GitHub username. The button cannot deploy a ZIP file directly.

A Telegram group collection game adapted from Waifu Catcher. Players collect Bollywood actresses by guessing their names, earn coins, trade cards, duel, and compete on leaderboards.

## Features
- Timed and message-count actress drops in groups
- `/guess <actress name>` to collect the active actress
- `/collection` and `/harem` to browse your collection
- `/profile`, `/fav`, `/daily`, `/balance`
- Marketplace: `/market`, `/sell`, `/buy`, `/delist`
- Social play: `/trade`, `/gift`, `/duel`
- Rankings: `/top`, `/ctop`, `/TopGroups`
- Admin upload: `/addactress` (also `/upload`), `/uploadchar`, `/delete`, `/update`
- Inline collection search, group drop settings, broadcast and admin tools

## Requirements
- Python 3.10 or 3.11
- MongoDB connection string
- Telegram bot token from @BotFather
- A Telegram group for logs and a channel where actress cards are posted

## Local setup
```bash
git clone https://github.com/botifyx-bots/WAIFU-HUSBANDO-CATCHER
cd WAIFU-HUSBANDO-CATCHER
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Fill in .env, then run:
python -m waifu
```

## Environment variables
| Variable | Required | Description |
|---|---:|---|
| `BOT_TOKEN` | Yes | Telegram bot token |
| `BOT_USERNAME` | Yes | Bot username without @ |
| `OWNER_ID` | Yes | Numeric Telegram user ID |
| `SUDO_IDS` | No | Comma-separated numeric admin IDs |
| `GROUP_ID` | Yes | Log group chat ID |
| `CHARA_CHANNEL_ID` | Yes | Actress-card channel ID; bot must be admin |
| `MONGO_URI` | Yes | MongoDB connection URI |
| `DB_NAME` | No | Defaults to `actress_arena_gold` |
| `SUPPORT_CHAT` | No | Support chat username |
| `UPDATE_CHAT` | No | Updates channel username |
| `PHOTO_URLS` | No | Comma-separated fallback image URLs |
| `DROP_INTERVAL_MINUTES` | No | Timed drop interval, default 15 |
| `DEFAULT_MSG_FREQUENCY` | No | Group messages per drop, default 100 |

## Add an actress
Admin command format:
```text
/addactress IMAGE_URL Actress-Name Bollywood 3
```
Rarity: `1` Common, `2` Rare, `3` Legendary, `4` Medium, `5` Special Edition.

Or post an image in the configured actress channel with this caption, then reply to that post with `/uploadchar`:
```text
🍀 Name: Deepika Padukone
🍋 Rarity: Legendary
🎬 Category: Bollywood
🌱 ID: 26
```
`ID` is optional. `Category` may also be `Actress Category`; legacy `Anime` captions are accepted for compatibility.

## Heroku deployment
This project uses a worker process (not a web server). Upload this folder to a **public GitHub repository** first, then use the Deploy button above. The `app.json` defines the required Config Vars and requests one worker dyno. Confirm the environment values on Heroku, provide a reachable MongoDB URI, and deploy. The included `Procfile` starts the worker with `python -m waifu`. If the worker is not running after deployment, open Heroku **Resources** and enable the `worker` dyno.

## Important security note
Never commit `.env`. Keep bot tokens and database credentials in platform Config Vars. If a token or database URI has been shared publicly, rotate it immediately.

## Database
The default database is `actress_arena_gold`; actress documents are stored in the `actresses` collection. Existing internal `anime` metadata is replaced with `category` in this adapted schema.
