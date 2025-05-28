import requests
import json
import time
from datetime import datetime
from pathlib import Path

print(f"-----------------Script started at:{datetime.now()}------------------")

#===========Configuration============#
# Enter your URLScan.io API key
API_KEY = 'ENTER_YOUR_URLSCAN_API_KEY_HERE'

# Enter your Telegram bot token (from @BotFather)
TG_BOT_TOKEN = 'ENTER_YOUR_TELEGRAM_BOT_TOKEN_HERE'

#Enter your Telegram chat ID (can be a user ID or group ID)
TG_CHAT_ID = 'ENTER_YOUR_TELEGRAM_CHAT_ID_HERE'

# File to store already seen scan UUIDs to avoid duplicate alerts
LAST_SEEN_FILE = 'seen_results.json'


#============Brand Queries===========#
# Customize these queries based on brands you want to monitor. Enter proper URLScan.io search query syntax.
BRAND_QUERIES = {
    "YesBank": [
        'page.title:"Yes Bank" AND NOT page.domain:yesbank.in AND date:>now-1d',
    ],
    "ShoppersStop": [
        'page.title:"Shoppers Stop" AND NOT page.domain:shoppersstop.com AND date:>now-1d',
    ],
    "RBI": [
        'page.title: "Reserve Bank of India" AND NOT rbi.org.in AND NOT blogspot.com AND date:>now-1d',
    ],
    "ICICI": [
        'page.title:"ICICI" AND NOT icicibank.com AND date:>now-1d'
    ]
}

#=============FUNCTIONS===============#
def load_seen():
	if Path(LAST_SEEN_FILE).exists():
		with open(LAST_SEEN_FILE,'r') as f:
			return json.load(f)
	return {}

def save_seen(data):
	with open(LAST_SEEN_FILE,'w') as f:
		json.dump(data,f)

def send_telegram_message(text, image_url=None):
    requests.post(f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage', data={
        'chat_id': TG_CHAT_ID,
        'text': text
    })
    if image_url:
        requests.post(f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendPhoto', data={
            'chat_id': TG_CHAT_ID,
            'photo': image_url
        })

def check_brand_scans():
    headers = {'API-Key': API_KEY}
    seen = load_seen()
    new_seen = seen.copy()

    for brand, queries in BRAND_QUERIES.items():
        for query in queries:
            print(f"[+] Checking {brand} for query: {query}")
            resp = requests.get(f'https://urlscan.io/api/v1/search/?q={query}', headers=headers)
            results = resp.json().get('results', [])

            for r in results:
                uuid = r['_id']
                if uuid in seen:
                    continue  # Skip already seen

                title = r['page'].get('title', 'No Title')
                verdict = r.get('verdicts', {}).get('overall', {}).get('score', 'N/A')
                screenshot_url = r.get('screenshot', None)
                result_url = f"https://urlscan.io/result/{uuid}"

                message = (
                    f"**[{brand}] New Phishing Scan Found**\n"
                    f"Title: {title}\n"
                    f"Score: {verdict}\n"
                    f"Query: {query}\n"
                    f"Link: {result_url}"
                )

                send_telegram_message(message, screenshot_url)
                new_seen[uuid] = True

    save_seen(new_seen)

# ============== MAIN ===============#

if __name__ == "__main__":
    check_brand_scans()
