from bs4 import BeautifulSoup
import time
import requests
import re
import ssl
import smtplib
import datetime
import http.cookiejar as cookielib

headers = {
    'authority': 'q.utoronto.ca',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-CA,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': '_gcl_au=1.1.1096831204.1598468780; unsupported_browser_dismissed=true; log_session_id=299e1b7566d3a0f7d666eefdf7e8fb20; _ga_4Q2ZJ2TF9M=GS1.1.1604438761.5.0.1604438763.0; _ga=GA1.2.1361537785.1587595080; _gid=GA1.2.962579474.1604626424; _legacy_normandy_session=Gg7ubelW3EGuNVEB-UKbuA+jFV8rLeVPzT4V9y-xPPkOHwW1v57--eOb2GX-G8PvfIAzuAPKRXB-pyeJrkTVbyQk3i4-yYncxkxmSKTd47h_X-d6tukjzporBs8Wa_ZEopTY3i6ifpyZ_SzE3jcMxfG0l4rfs7jIm1Awlzuwt6GrgnlxCTsRtTqJGlFxDawtkWkUMyyUsBImfgv8qdjYlMT5YVOzKid6TfiB2Ns4ip4GLK_LeDGUA58zDo5GFK9BXCYCKI5lR8-YoO83zkBtn1b2FtiNsQnpw832w5_ulsOssADqYzqON5Kpwzfk5nRuoYVOVkVgNZfvc2r1p5plV_BWoPpAsm1_ZK3ffohqlF_ArcFZhnlMG_Wx-VPDwXPDq52WHB4kYApTjjhoJagrGWvx04M2ifBkRqaTeqZB6YahdTsKJ2ZS-x92Nr5x7jag8znlIKTj0yJepHpFw6nySvCrnQg4f48TjGQ4ReETYYqy_MtsDaWc3jrSuhrepBzHIp3YMOqlyVS-swGChsXNGjeiphn2QF2A23KtEFA9AJB1-INsiZ4SczE_d--O-Pxrpd5Rf3HkKCtgKcl1yG2PEurQbkulEQpWfXKfJQKWq_jIsoOH7EE-ZKtGfaW1GCiN9SgFM5-41IP8x9uAaYBV2IdGhTNIlF-3EociTsRV9nLFLEw9cpwmaL68wmz3a58BEO41-fLovmTqAnw7y_n0RBY0X-k0ciyN9SuafGlJk_620gbxpkkRAUOE-AcDCuVmFx_ZLoDWeXD0Plzo5doixYId8FglKpbaG6e1hECUwGsqtfvGPXez94RlKtJlGGpoFvtylfHx2pM3Ko5mU-PAmV6tfRh6QFinXB_Cdycxm7nViVhS5f87UZ5eVcWlITVVcsTYnNTvwLTEzwhRcXFP9eh.aFKX_QHgepcaKZ-c4L5MIWlCj4c.X6cPgQ; canvas_session=Gg7ubelW3EGuNVEB-UKbuA+jFV8rLeVPzT4V9y-xPPkOHwW1v57--eOb2GX-G8PvfIAzuAPKRXB-pyeJrkTVbyQk3i4-yYncxkxmSKTd47h_X-d6tukjzporBs8Wa_ZEopTY3i6ifpyZ_SzE3jcMxfG0l4rfs7jIm1Awlzuwt6GrgnlxCTsRtTqJGlFxDawtkWkUMyyUsBImfgv8qdjYlMT5YVOzKid6TfiB2Ns4ip4GLK_LeDGUA58zDo5GFK9BXCYCKI5lR8-YoO83zkBtn1b2FtiNsQnpw832w5_ulsOssADqYzqON5Kpwzfk5nRuoYVOVkVgNZfvc2r1p5plV_BWoPpAsm1_ZK3ffohqlF_ArcFZhnlMG_Wx-VPDwXPDq52WHB4kYApTjjhoJagrGWvx04M2ifBkRqaTeqZB6YahdTsKJ2ZS-x92Nr5x7jag8znlIKTj0yJepHpFw6nySvCrnQg4f48TjGQ4ReETYYqy_MtsDaWc3jrSuhrepBzHIp3YMOqlyVS-swGChsXNGjeiphn2QF2A23KtEFA9AJB1-INsiZ4SczE_d--O-Pxrpd5Rf3HkKCtgKcl1yG2PEurQbkulEQpWfXKfJQKWq_jIsoOH7EE-ZKtGfaW1GCiN9SgFM5-41IP8x9uAaYBV2IdGhTNIlF-3EociTsRV9nLFLEw9cpwmaL68wmz3a58BEO41-fLovmTqAnw7y_n0RBY0X-k0ciyN9SuafGlJk_620gbxpkkRAUOE-AcDCuVmFx_ZLoDWeXD0Plzo5doixYId8FglKpbaG6e1hECUwGsqtfvGPXez94RlKtJlGGpoFvtylfHx2pM3Ko5mU-PAmV6tfRh6QFinXB_Cdycxm7nViVhS5f87UZ5eVcWlITVVcsTYnNTvwLTEzwhRcXFP9eh.aFKX_QHgepcaKZ-c4L5MIWlCj4c.X6cPgQ; _csrf_token=8JrlUwG00gU1er%2FSEhuO7taQglWHjnKL7CjXLYxnt7a67owrRoK%2FSFQphpsheduaoNO3Y9%2B3EMDcS49BtB3f4Q%3D%3D',
}

assignments = {}
months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May': 5, 'Jun': 6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

def update_due_dates():
	"""
	This function looks for upcoming assignments/quizes and adds them to 'assignments'.
	This function assumes that all due dates are in the current year. 
	"""
	response = requests.get('https://q.utoronto.ca/courses/176147/grades', headers=headers)
	#print(response.content)
	soup = BeautifulSoup(response.content, features="html5lib")

	table = soup.find( "table", {"id":"grades_summary"} )
	dues = []
	global due_dates
	for row in table.findAll("tr"):
		due_date = row.find(attrs={"class":'due'})
		if due_date is not None:
			str_date = format_date(due_date.get_text())
			if str_date != "":
				year = datetime.datetime.today().year
				month = months[str_date[0:3]]
				day = str_date[4:6]
				day = day.strip()
				day = int(day)
				if ':' in str_date:
					hour = int(str_date[-7:-5])
					minute = int(str_date[-4:-2]) 
				else:
					hour = int(str_date[-4:-2])
					minute = 0
				if str_date[-2:] == 'pm':
					hour += 12
				datetime_date = datetime.datetime(year, month, day, hour, minute)
				assignment_title = row.find(attrs={"class":"title"})
				assignment_title = row.find('a').get_text()
				# check if assignment is due in the future
				if assignment_title not in assignments and datetime_date > datetime.datetime.today():
					assignments[assignment_title] = datetime_date



def format_date(date):
	date = date[2:]
	date = date.strip()
	return date

def email_user(sender_email, password):
	"""
	This function will email the user if an upcoming assignment is due in the next 24 hours
	"""
	successfully_emailed = []
	for assignment in assignments:
		day_before_due_date = assignments[assignment] - datetime.timedelta(days=1)
		if datetime.datetime.today() >= day_before_due_date:
		# if 1: # For testing purposes
			smtp_server = "smtp.gmail.com"
			port = 587
			
			context = ssl.create_default_context()

			try:
				server = smtplib.SMTP(smtp_server, port)
				server.ehlo()
				server.starttls(context=context)
				server.ehlo()
				server.login(sender_email, password)

				subject = f'{assignment} due soon!'
				body = f'{assignment} is due at {assignments[assignment]}'
				message = f"Subject: {subject}\n\n{body}"

				server.sendmail(
					sender_email,
					sender_email,
					message
				)

			except Exception as e:
				print(e)
			finally:
				server.quit()

			successfully_emailed.append(assignment)
	for assignment in successfully_emailed:
		del assignments[assignment]
	successfully_emailed = []

if __name__ == '__main__':
	email = input("Type your Gmail address and press enter: ")
	password = input("Type your password and press enter: ")
	while(1):
		update_due_dates()
		email_user(email, password)
		time.sleep(60*60*6)
