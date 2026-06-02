# Epic Games Free Game Auto-Claimer

A Python tool that runs on a GitHub Actions cron schedule to detect and automatically claim newly available free games on the Epic Games Store using browser-based session cookies and Playwright.

## Features
- **Auto-Claiming**: Checks Epic Games Store for free games and claims them automatically via Playwright headless Chromium.
- **Cookie Authentication**: Operates entirely on user session cookies without needing a username/password or solving CAPTCHAs during the automated run.
- **GitHub Secrets Sync**: Uses PyNaCl to securely re-encrypt and update the `EPIC_COOKIES` secret inside GitHub whenever cookies are refreshed by Epic.
- **Telegram Notifications**: Sends Telegram messages to notify you of successful claims, missing cookies, or CAPTCHA challenges requiring human intervention.
- **State Tracking**: Records claimed game `offer_id`s to avoid redundant claiming.

## Getting Started

1. Clone this repository to your own GitHub account.
2. Run `pip install -r requirements.txt` and `playwright install chromium` locally.
3. Run `python scripts/export_cookies.py`. A browser will open; log in to your Epic Games account and solve any CAPTCHAs. The script will output a JSON array of your cookies.
4. Go to your GitHub repository settings > Secrets and variables > Actions. Add the following repository secrets:
   - `EPIC_COOKIES`: The JSON output from step 3.
   - `TELEGRAM_BOT_TOKEN`: The token for your Telegram Bot.
   - `TELEGRAM_CHAT_ID`: Your Telegram Chat ID.
   - `GITHUB_TOKEN` (optional but recommended): A Personal Access Token with repository write permissions to update the cookie secret.
5. The GitHub Action will run automatically every Thursday at 9 AM UTC and 5 PM UTC, and Mondays at 9 AM UTC.

## Local Execution
Create a `.env` file from `config.example.env` and populate the variables, including pasting your JSON array directly into `EPIC_COOKIES`.
Run the script locally using:
```bash
python -m claimer
```
