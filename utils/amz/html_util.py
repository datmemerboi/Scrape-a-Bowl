"""
All HTML based utils
"""
import os

from bs4 import BeautifulSoup
import urllib.request as Request

def HtmlUtil(url):
	"""
	Util to fetch HTML of a URL

	Params: URL
	Returns: HTML webpage of the URL as string
	"""
	opener = Request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0 Safari/537.36')]
	response = opener.open(url)

	try:
		sourceHtml = BeautifulSoup(response.read(), 'html.parser')
		print("[UTIL] HTML obtained from {} successfully".format(url))
		return str(sourceHtml)

	except Exception as err:
		print("[UTIL] Faced error in fetch HTML: \n {}".format(err))
		return None

def HtmlFileUtil(url):
	"""
	Util to fetch HTML of a URL and write to file

	Params: URL
	Returns: path/to/html/file
	"""
	opener = Request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0 Safari/537.36')]
	response = opener.open(url)
	try:
		html = BeautifulSoup(response.read(), 'html.parser')
		print("[UTIL] HTML obtained from {} successfully".format(url))
		currentHtmlPath = os.path.join(os.path.dirname(__file__), '..', '..', 'html')
		if not os.path.exists(currentHtmlPath):
			os.makedirs(currentHtmlPath)

		with open(os.path.join(currentHtmlPath, 'current.html'), 'w+') as file:
			file.write(str(html))
			print("[UTIL] HTML file created!")
			file.close()

		return os.path.abspath(os.path.join(currentHtmlPath, 'current.html'))
	except Exception as err:
		print("[UTIL] Faced error in fetch HTML: \n {}".format(err))
		return False