import requests
token = "Bearer {0zSipJOagIqfAXU8_ZsNN0mRmz-N0L31-ycmBQo9cuoAAAF9TdmcPQ}"
response = requests.post(url="https://kapi.kakao.com/v2/user/me", headers={'Authorization': token})
print(response.json())