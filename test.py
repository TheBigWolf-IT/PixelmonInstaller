from urllib import request


import json
import requests

url = 'https://raw.githubusercontent.com/TheBigWolf-IT/PixelmonInstaller/main/testurl'
resp = requests.get(url)
data = json.loads(resp.text)
profile_url = data['profiles']
pack_url = data['pack']
print(pack_url)
print(profile_url)
