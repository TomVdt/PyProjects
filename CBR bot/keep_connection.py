import requests
from env import *

cookies = {
    'dtCookie': COOKIE,
    'JSESSIONID': JSESSIONID,
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.cbr.nl/nl/mijncbr/reserveren.htm?type=wijzigen&product_code=BTH',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
}

response = requests.get('https://www.cbr.nl/nl/mijncbr/session-refresh.htm', headers=headers, cookies=cookies)

print(response)
