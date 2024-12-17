import requests

url = "https://free-cricket-live-score1.p.rapidapi.com/schedule/upcoming"
payload = {
    "page_number": 1,
    "match_formate": "T20"
}
headers = {
    "x-rapidapi-key": "8467044fdemsh1a4a175854aad63p19cea2jsn5961618649b1",
    "x-rapidapi-host": "free-cricket-live-score1.p.rapidapi.com",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print(response.content)
