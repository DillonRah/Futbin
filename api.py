import requests 
import json


def upgrade_to_bot_account(token):
    url = "https://lichess.org/api/bot/account/upgrade"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        print("Account successfully upgraded to bot account.")
    else:
        print(f"Failed to upgrade account. Status code: {response.status_code}")

# Replace <yourTokenHere> with your actual Lichess API token
your_token = "<lip_aO2neoPU45kTorbEbWX9>"
upgrade_to_bot_account(your_token)


token = "lip_aO2neoPU45kTorbEbWX9"
headers = {"Authorization": f"Bearer {token}"}
url = "https://lichess.org/api/account"
print(requests.get(url, headers=headers, stream=True).json())
