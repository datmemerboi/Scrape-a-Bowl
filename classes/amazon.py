"""
Amazon Class
"""
import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.amz.html_util import HtmlUtil, HtmlFileUtil
from utils.amz.search_util import SearchDomainForKeyword
from utils.amz.product_util import ProductUtil, ProductFileUtil

class Amazon():
	"""
	Class for all Amazon related requests
	Methods Used:
		ProductDeatils : obtains product details
		ProductDetailsAsFile : obtains product details and stores as file
		KeywordSearch : obtains details from keyword search results
	"""
	def __init__(self, url=None):
		self.url = url

	def ProductDetails(self, url=None):
		"""
		Fn to fetch details of an amazon product

		Params: URL or None(if URL mentioned at __init__)
		Returns: Product details as JSON object
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
			print("[AMAZON] ProductDetails error: \n {}".format(err))
			return None

	def ProductDetailsAsFile(self, url = None):
		"""
		Fn to fetch and store details of an amazon product

		Params: URL or None(if URL mentioned at __init__)
		Returns: Stores the JSON in a file and returns path/to/file.json
		"""
		if self.url is None and url is None:
			print("[AMAZON] Error: No URL mentioned")
			return None

		url = self.url if url is None or len(url) < 2 else url

		try:
			htmlFilePath = HtmlFileUtil(url)
			print("[AMAZON] HTML file stored in path {}".format(os.path.abspath(htmlFilePath)))
			productFilePath = ProductFileUtil(htmlFilePath, url)
			if productFilePath:
				print("[AMAZON] ProductObject file stored in path {}".format(os.path.abspath(productFilePath)))
				return True
			print("[AMAZON] ProductObject found to be {}".format(productFilePath))
			return False
		except Exception as err:
			print("[AMAZON] ProductDetailsAsFile error: \n {}".format(err))
			return None

	def KeywordSearch(self, keyword, domain = None, limit = None):
		"""
		Fn to fetch search results for a keyword

		Params: keyword, domain(optional, URL from __init__), limit(optional)
		Returns: search result as JSON object
		"""
		if len(keyword) < 2 or keyword is None:
			print("[AMAZON] Error: No keyword mentioned")
			return None

		if self.url is None and domain is None:
			print("[AMAZON] Error: No URL / domain mentioned")
			return None

		try:
			domain = re.findall(r"amazon\.\w{2,3}[\.\w{2,3}]*", domain)[0]\
				if domain is not None\
				else re.findall(r"amazon\.\w{2,3}[\.\w{2,3}]*", self.url)[0]
			return SearchDomainForKeyword(domain, keyword, limit)
		except Exception as err:
			print("[AMAZON] KeywordSearch error: \n {}".format(err))
			return None