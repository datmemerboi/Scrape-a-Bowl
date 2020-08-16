def HtmlUtil(url):
	import urllib.request as Request; from bs4 import BeautifulSoup;

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
	import os; from bs4 import BeautifulSoup;
	import urllib.request as Request

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