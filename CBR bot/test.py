import requests
import time
import threading


def do_post():
	cookies = {
		'_aha_ses.b3a8': '*',
		'_aha_id.b3a8': '670cdf96-ab44-485e-b219-cb43852770bc.1631634697.1.1631634697.1631634697.f0cb8896-a206-4629-848c-47b6221578dd',
		'AWSALB': 'T1wE+9s53PIuufwFPcam7aURUbnGPFzTYHoVMqak20wk1Wu/4TiPzty9MlLYGamNUSXBrQC8MoH7skj+zu21aa2dKFecMvJ8c+XcFb7oxRQ2UGm+xIYbHiKHlj8v',
		'AWSALBCORS': 'T1wE+9s53PIuufwFPcam7aURUbnGPFzTYHoVMqak20wk1Wu/4TiPzty9MlLYGamNUSXBrQC8MoH7skj+zu21aa2dKFecMvJ8c+XcFb7oxRQ2UGm+xIYbHiKHlj8v',
	}

	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
		'Accept': 'application/json, text/plain, */*',
		'Accept-Language': 'en-US,en;q=0.5',
		'Content-Type': 'application/json;charset=utf-8',
		'X-Requested-With': 'XMLHttpRequest',
		'Origin': 'https://audience.ahaslides.com',
		'DNT': '1',
		'Connection': 'keep-alive',
		'Referer': 'https://audience.ahaslides.com/86q19z8ajf',
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin',
		'Sec-GPC': '1',
		'TE': 'trailers',
	}

	data = '{"audienceId":"99a7e16446a54a87ad42645f65a07b30","audienceName":"","slideId":40785966,"presentationId":1987718,"reactionType":"heart"}'

	response = requests.post('https://audience.ahaslides.com/api/reaction/', headers=headers, cookies=cookies, data=data)
	if response.json()['code'] != 'ok':
		print('Failed.')


MAX_THREADS = 30
total = 0
threads = 0
while total < 69000:
	if threading.active_count() < MAX_THREADS:
		stonks = threading.Thread(target=do_post)
		stonks.start()
		total += 1
while threading.active_count() > 0:
	time.sleep(0.5)
