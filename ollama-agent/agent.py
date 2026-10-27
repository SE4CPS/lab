import requests

API_KEY = "15b06c28b2fd45c5891dd113299f3ebd.oFYb-yFv5KsebHNNrs53AL9B"

url = "https://api.ollama.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "ministral-3:8b",
    "messages": [
        {"role": "user", "content": "Say hello world."}
    ],
    "temperature": 0
}

response = requests.post(url, headers=headers, json=payload)

print("Status Code:", response.status_code)
print("Response Text:", response.text)