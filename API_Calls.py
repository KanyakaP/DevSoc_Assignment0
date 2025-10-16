import os
import json
import requests
api_key = os.getenv("GeminiKey")
if not api_key:
    raise ValueError("No API key found. Did you export GeminiKey?")
url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
headers = {"Content-Type": "application/json"}

with open("input.txt", "r", encoding="utf-8") as f:
    prompts = [line.strip() for line in f if line.strip()]

responses = []
for prompt in prompts:
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        try:
            text_response = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            text_response = "No response from API"
    else:
        text_response = f"Error {response.status_code}: {response.text}"

    responses.append({
        "prompt": prompt,
        "response": text_response
    })

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(responses, f, indent=4, ensure_ascii=False)

print("All responses saved to output.json")
