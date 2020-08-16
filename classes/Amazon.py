import os, sys, re;
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.amz.html_util import HtmlUtil, HtmlFileUtil
from utils.amz.product_util import ProductUtil, ProductFileUtil
from utils.amz.search_util import SearchDomainForKeyword, ExtractFromCard, ListOfCardObjects

class Amazon(object):
	def __init__(self, url=None):
		self.url = url

	def ProductDetails(self, url=None):
		if self.url == None and url == None:
			print("[AMAZON] Error: No URL mentioned")
			return None

		url = self.url if url == None or len(url) < 2 else url
		try:
			sourceHtml = HtmlUtil(url)
			if(sourceHtml):
				productObj = ProductUtil(sourceHtml, url)
				return productObj

			else:
				raise Exception("No HTML data returned")

		except Exception as err:
			print("[AMAZON] ProductDetails error:")
			print(err)
			return None

	def ProductDetailsAsFile(self, url=None):
		if self.url == None and url == None:
			print("[AMAZON] Error: No URL mentioned")
			return None

		url = self.url if url == None or len(url) < 2 else url
		try:
			htmlFilePath = HtmlFileUtil(url)
			print("[AMAZON] HTML file stored in path {}".format(str(htmlFilePath)))
			productFilePath = ProductFileUtil(htmlFilePath, url)
			print("[AMAZON] ProductObject file stored in path {}".format(str(productFilePath)))
			return True

		except Exception as err:
			print("[AMAZON] ProductDetailsAsFile error:")
			print(err)
			return None

	def KeywordSearch(self, keyword, url=None, limit=None):
		if len(keyword) < 2 or keyword == None:
			print("[AMAZON] Error: No keyword mentioned")
			return None

		if self.url == None and url == None:
			print("[AMAZON] Error: No URL mentioned")
			return None

		url = self.url if url == None or len(url) < 2 else url
		try:
			domain = re.findall(r"^https://www\.amazon\.\w{2,3}[\.\w{2,3}]*", url)
			if not len(domain):
				raise Exception("Invalid domain of URL. Must be of form 'https://www.amazon.in/'")
			domain = domain[0].replace('https://','')

			return SearchDomainForKeyword(domain, keyword, limit)
		
		except Exception as err:
			print("[AMAZON] KeywordSearch error:")
			print(err)
			return None