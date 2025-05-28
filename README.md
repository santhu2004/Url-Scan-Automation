# Url-Scan-Automation
 A Python script to monitor phishing attempts using URLScan.io and send alerts via Telegram. Designed for security researchers and threat intel.

🚀 Features

Monitors recent URLScan.io results for signs of phishing.

Filters out legitimate domains using custom search queries.

Sends alerts on Telegram with:

- Site title

- Screenshot

- URLScan result link

Avoids duplicate alerts using a local JSON cache.

🔧 Setup

1. Clone this repository

<pre>git clone https://github.com/santhu2004/Url-Scan-Automation.git
cd Url-Scan-Automation </pre>

2. Install dependencies

pip install requests

3. Configure your credentials

Open the Python script (automation.py) and replace the placeholders at the top of the file:

#===========Configuration============#

#  Enter your URLScan.io API key
API_KEY = 'ENTER_YOUR_URLSCAN_API_KEY_HERE'

#  Enter your Telegram bot token (create from @BotFather)
TG_BOT_TOKEN = 'ENTER_YOUR_TELEGRAM_BOT_TOKEN_HERE'

#  Enter your Telegram chat ID
TG_CHAT_ID = 'ENTER_YOUR_TELEGRAM_CHAT_ID_HERE'

You can also modify the BRAND_QUERIES dictionary to add or adjust the brands and search queries you want to monitor.


⏱️ Running Automatically with Cron

You can run the script periodically using a cron job for proactive monitoring.

Example: Run every 30 minutes

Open the crontab:

crontab -e

Add the following line:

*/30 * * * * /usr/bin/python3 /path/to/Url-Scan-Automation/automation.py >> /path/to/log.txt 2>&1

📝 Make sure to replace /path/to/... with the actual full path to your Python script and Python executable.

📁 Output File

The script creates and updates seen_results.json to store previously alerted scans and avoid duplicates.

🤝 Contributions

Pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to change.
