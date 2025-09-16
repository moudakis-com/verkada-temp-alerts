import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

api_key = os.getenv('VERKADA_API_KEY')
device_id = os.getenv('DEVICE_ID')
webhook_url = os.getenv('WEBHOOK_URL')

def get_login():
    login_url = "https://api.verkada.com/token"
    headers = {
        "accept": "application/json",
        "x-api-key": api_key
    }

    response = requests.post(login_url, headers=headers)
    data = response.json()
    return(data)

def get_temp(login_key, prev_temp):
    request_url = f"https://api.verkada.com/environment/v1/data?device_id={device_id}&page_size=1&fields=temperature&interval=5s"

    key = login_key["token"]
    headers = {
        "accept": "application/json",
        "x-verkada-auth": key
    }

    try:
        response = requests.get(request_url, headers=headers)
        data = response.json()

    except:
        print("ERR: Failed to fetch temperature. Falling back to last known temperature. API response below...")
        print("-----")
        print(data)
        temp_f = prev_temp

    temp_c = data["data"][0]["temperature"]
    temp_f = (temp_c * 9/5) + 32
        
    return(temp_f)

def send_webhook(payload):
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status() 

        print(f"Webhook sent successfully! Status Code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook: {e}")

def alert(prev_temp):
    limit = 90
    temp = get_temp(get_login(), prev_temp)
    if int(temp) >= limit and prev_temp < limit:
        payload = {
            "content": "ALERT: Temperature Warning",
            "username": "Sensor-Alerts",
            "embeds": [
                {
                    "title": f"Network Rack at {round(temp, 2)}°F",
                    "description": "A follow up alert will trigger when stabilized",
                    "color": 16711680 # Red color
                }
            ]
        }
        send_webhook(payload)
    elif int(temp) >= limit and prev_temp >= limit:
        pass
    elif int(temp) < limit and prev_temp >= limit:
        payload = {
            "content": "RESOLVED: Temperature Warning",
            "username": "Sensor-Alerts",
            "embeds": [
                {
                    "title": f"Network Rack at {round(temp, 2)}°F",
                    "description": "The temperature has stabilized.",
                    "color": 33024 # Green color
                }
            ]
        }
        send_webhook(payload)
    else:
        pass
    prev_temp = temp
    return prev_temp

def main():
    last_temp = 0
    while True:
        last_temp = alert(last_temp)
        time.sleep(10)


main()
