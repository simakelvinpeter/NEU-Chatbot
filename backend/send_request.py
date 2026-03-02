import requests
resp = requests.post("http://localhost:8000/api/chat", json={"session_id":"test","message":"Tell me a joke about universities.","language":"EN"})
print(resp.status_code, resp.text)
