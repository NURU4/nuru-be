import requests
key = "jKmqyMwLo9oycSqXyanqGT1iECUIV5CN0JDZ6Ao9dVwAAAF9UAygFA"
token = "Bearer {" + key + "}"
response = requests.post(url="https://kapi.kakao.com/v2/user/me", headers={'Authorization': token})
print(response.json())