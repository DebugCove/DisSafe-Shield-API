import os
from dotenv import load_dotenv
import requests


load_dotenv()
TOKEN = os.getenv("TOKEN")
TIMEOUT = 5

user_id = input("Enter the user ID: ")
username = input("Enter the username: ")

url = f"https://discord.com/api/v10/users/{user_id}"
headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}

try:
    response = requests.get(url, headers=headers, timeout=TIMEOUT)
except requests.exceptions.Timeout:
    print("Request timed out.")
    exit()
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    exit()

if response.status_code == 200:
    user_data = response.json()
    actual_username = user_data["username"]

    if actual_username == username:
        print("The username matches the provided user ID.")
    else:
        print("The username does not match the provided user ID.")
elif response.status_code == 404:
    print("User not found.")
else:
    print(f"Error: {response.status_code}")
