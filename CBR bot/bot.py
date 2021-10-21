import requests
import datetime
import time
import telegram_send
from env import *


locations = {
	'Rijswijk Zh': '22-03-5',
	'Rijswijk Zh EXTRA': '22-01-3'
}

start_date = datetime.datetime.today()
current_test_time = datetime.datetime.strptime(EXAM_DAY, '%Y,%m,%d,%H,%M')


def do_request(date, location):
	cookies = {
	'dtCookie': COOKIE,
	'JSESSIONID': JSESSIONID,
	}

	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
		'Accept': 'application/json',
		'Accept-Language': 'en-US,en;q=0.5',
		'Referer': 'https://www.cbr.nl/nl/mijncbr/reserveren.htm?type=wijzigen&product_code=BTH',
		'X-Requested-With': 'XMLHttpRequest',
		'Expires': '-1',
		'Cache-Control': 'no-cache,no-store,must-revalidate,max-age=-1,private',
		'DNT': '1',
		'Connection': 'keep-alive',
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin',
		'Sec-GPC': '1',
	}

	params = (
		('product_code', 'BTH'),
		('location', locations[location]),
		('selected_date', date),
		('hash', HASH),
		('t-id', T_ID),
	)

	print(f'Getting available timestamps for {date} at {location}')
	response = requests.get('https://www.cbr.nl/web/business/coordinator/application/reservation/stage/getavailablecapacity', headers=headers, params=params, cookies=cookies)

	if response:
		return response.json()
	else:
		return None


def parse(response):
	extracted = []
	for data in response['data']['nestedValueObjects']:
		info = {}
		for entry in data['valueObjectInformation']['entry']:
			if entry['key'] == 'end_date_time':
				info['end'] = datetime.datetime.fromtimestamp(int(entry['value'][:10]))
			if entry['key'] == 'start_date_time':
				info['start'] = datetime.datetime.fromtimestamp(int(entry['value'][:10]))
			if entry['key'] == 'location_code':
				info['location'] = {v: k for k, v in locations.items()}[entry['value']]

		extracted.append(info)
	return extracted


def log_response(response):
	if response:
		if response['success']:
			dates = parse(response)
			if len(dates) > 0:
				for date in dates:
					if date['start'] < current_test_time:
						print(f'Found available place at {date["location"]} on {date["start"].strftime("%A %d %B %Y at %H:%M")}')
						telegram_send.send(messages=[f'New date for CBR theorie-examen found: at {date["location"]} on {date["start"].strftime("%A %d %B %Y at %H:%M")}!'])
			else:
				print('No places found.')
		else:
			print('Logged in from other location')
	else:
		print('Request failed, maybe got logged out?')


def main():
	print(datetime.datetime.today().strftime('%A %d %B %Y, %H:%M'))
	for location in locations.keys():
		request_date = start_date
		i = 0
		while request_date < current_test_time:

			response = do_request(request_date.strftime('%d-%m-%Y'), location)
			log_response(response)

			i += 1
			request_date += datetime.timedelta(days=14)

			time.sleep(3)


main()
