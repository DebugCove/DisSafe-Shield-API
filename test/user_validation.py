import os
from dotenv import load_dotenv
import requests

load_dotenv()
# Discord bot token (not user token)
TOKEN = os.getenv('TOKEN')
TIMEOUT = 5

USER_ID = 'USER_ID_HERE'
url = f'https://discord.com/api/v10/users/{USER_ID}'


headers = {
    'Authorization': f'Bot {TOKEN}', 
    'Content-Type': 'application/json'
}


response = requests.get(url, headers=headers, timeout=TIMEOUT)


if response.status_code == 200:
    print("User exists.")
elif response.status_code == 404:
    print("User not found.")
else:
    print(f'Error: {response.status_code}')
