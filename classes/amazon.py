"""
class Amazon definition
"""
import os
import sys
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.amz.html_util import HtmlUtil, HtmlFileUtil
from utils.amz.product_util import ProductUtil, ProductFileUtil
from utils.amz.search_util import SearchDomainForKeyword

class Amazon():
	"""
	Used to create an instance for any product related to amazon domain
	Methods:
		ProductDeatils : obtains product details
		ProductDetailsAsFile : obtains product details and stores as file
		KeywordSearch : obtains details from keyword search results
	"""
	def __init__(self, url=None):
		self.url = url

	def ProductDetails(self, url=None):
		"""
		Fetches details of an amazon product url
		Input: URL or None(if URL mentioned at __init__)
		Output: Product details as JSON object
		"""
		if self.url is None and url is None:
			print("[AMAZON] Error: No URL mentioned")
			return None

		url = self.url if url is None or len(url) < 2 else url
		try:
			sourceHtml = HtmlUtil(url)
			productObj = ProductUtil(sourceHtml, url)
			return productObj

		except Exception as err:
			print("[AMAZON] ProductDetails error:")
			print(err)
			return None

	def ProductDetailsAsFile(self, url=None):
		"""
		Fetches and stores details of an amazon product
		Input: URL or None(if URL mentioned at __init__)
		Output: Stores the JSON in a file and returns path/to/file.json
		"""
		if self.url is None and url is None:
			print("[AMAZON] Error: No URL mentioned")
			return None

		url = self.url if url is None or len(url) < 2 else url
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

	def KeywordSearch(self, keyword, domain=None, limit=None):
		"""
		Fetches search result details for a keyword
		Input: keyword, domain(optional, URL from __init__), limit(optional)
		Output: keyword search result as JSON object
		"""
		if len(keyword) < 2 or keyword is None:
			print("[AMAZON] Error: No keyword mentioned")
			return None

		if self.url is None and domain is None:
			print("[AMAZON] Error: No URL / domain mentioned")
			return None

		try:
			domain = domain\
				if domain is not None\
				else re.findall(r"amazon\.\w{2,3}[\.\w{2,3}]*", self.url)[0]

			return SearchDomainForKeyword(domain, keyword, limit)

		except Exception as err:
			print("[AMAZON] KeywordSearch error:")
			print(err)
			return None