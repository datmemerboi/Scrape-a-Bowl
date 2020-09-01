"""
All HTML based utils
"""
import os
import urllib.request as Request
from bs4 import BeautifulSoup

def HtmlUtil(url):
	"""
	Util to fetch HTML of a URL
	Input: URL
	Output: HTML of the URL as string
	"""
	opener = Request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	response = opener.open(url)

	try:
		sourceHtml = BeautifulSoup(response.read(), 'html.parser')
		print("[UTIL] HTML obtained from {} successfully".format(url))	
		return str(sourceHtml)

	except Exception as err:
		print("[UTIL] Faced error in fetch HTML:")
		print(err)
		return None

def HtmlFileUtil(url):
	"""
	Util to fetch HTML of a URL and write to file
	Input: URL
	Output: path/to/html/file
	"""
	opener = Request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	response = opener.open(url)
	try:
		html = BeautifulSoup(response.read(), 'html.parser')
		print("[UTIL] HTML obtained from {} successfully".format(url))
		
		if not os.path.exists(os.path.join(os.path.dirname(__file__), '..', '..', 'html')):
			os.makedirs(os.path.join(os.path.dirname(__file__), '..', '..', 'html'))
			
		with open(os.path.join(os.path.dirname(__file__), '..', '..', 'html', 'current.html'), 'w+') as file:
			file.write(str(html))
			print("[UTIL] HTML file created!")
			file.close()

		return os.path.join(os.path.dirname(__file__), '..', '..', 'html', 'current.html')

	except Exception as err:
		print("[UTIL] Faced error in fetch HTML:")
		print(err)
		return False