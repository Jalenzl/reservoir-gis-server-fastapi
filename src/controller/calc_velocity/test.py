from requests import post as requests_post
from json import loads as json_loads

url = "https://fastapi.vip.cpolar.cn/api/v1/clacFlowVelocity"
json1 = {
    "layer": 6,
    "time": 4
}
res = json_loads(requests_post(url, json=json1).text)

v_water = res['velocity_water']
v_oil = res['velocity_oil']

print(f'vwater: {v_water}')
print(f'voil: {v_oil}')
