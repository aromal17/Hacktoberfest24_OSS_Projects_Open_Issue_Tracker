import subprocess
import time
import re
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Define your curl commands
curl_commands = {
    "unkey": os.getenv('UNKEY_PROJECT_ISSUE_SEARCH_CURL'),
    "formbricks": os.getenv('FORMBRICKS_PROJECT_ISSUE_SEARCH_CURL'),
    "hanko": os.getenv('HANKO_PROJECT_ISSUE_SEARCH_CURL'),
    "openBB": os.getenv('OPENBB_PROJECT_ISSUE_SEARCH_CURL'),
    "twenty": os.getenv('TWENTY_PROJECT_ISSUE_SEARCH_CURL'),
    "papermark": os.getenv('PAPERMARK_PROJECT_ISSUE_SEARCH_CURL')
}

# Function to run curl command and return output
def run_curl_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout  # Capture the standard output of the curl command
    except Exception as e:
        print(f"Failed to run {command}: {e}")
        return ""

def send_telegram_message(message):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID') 
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
 
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Telegram message sent successfully!")
    else:
        print(f"Failed to send message. Status Code: {response.status_code}")

def check_curls_and_notify():
    for project_name, curl_command in curl_commands.items():
        print(f"Running curl for {project_name}:")
        response = run_curl_command(curl_command)
        if "0 Open" not in response:
            send_telegram_message(f"Issue found in \"{project_name}\" project")
        else:
            print(f"'0 Open' found in {project_name}'s response.")
        print("\n")

# Main loop: Run every minute
if __name__ == "__main__":
    while True:
        check_curls_and_notify()
        time.sleep(os.getenv('SLEEP_DURATION')) 
