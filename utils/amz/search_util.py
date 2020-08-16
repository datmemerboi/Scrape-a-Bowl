import re, copy; import json as JSON;

def ExtractFromCard(cardElement, domain):
	cardObj = { 'amazon_message':[], 'imageURLs':[] }
	
	''' ASIN '''
	if cardElement.get('data-asin'):
		cardObj['ASIN'] = str(cardElement.get('data-asin'))
	
	''' LINK '''
	if cardElement.find('a', class_="a-link-normal a-text-normal"):
		cardObj['url'] = domain + str(cardElement.find('a', class_="a-link-normal a-text-normal").get('href'))
	
	''' TITLE '''
	if cardElement.find('span', class_="a-size-medium a-color-base a-text-normal"):
		cardObj['title'] = cardElement.find('span', class_="a-size-medium a-color-base a-text-normal").text
		cardObj['name'] = cardElement.find('span', class_="a-size-medium a-color-base a-text-normal").text
	
	''' RATING '''
	if cardElement.find('span', attrs={"aria-label":re.compile(r"^\d\.\d out of \d stars$")}):
		cardObj['customer_rating'] = cardElement.find('span', attrs={"aria-label":re.compile(r"^\d\.\d out of \d stars$")}).get('aria-label')
	if cardElement.find('span', attrs={"aria-label":re.compile(r"^\d+$")}):
		cardObj['customer_rating_count'] = int(cardElement.find('span', attrs={"aria-label":re.compile(r"^\d+$")}).get('aria-label').replace(',',''))
	
	''' PRICE '''
	if cardElement.find('span', attrs={"class":"a-price", "data-a-color":"price"}) and cardElement.find('span', attrs={"class":"a-price", "data-a-color":"price"}).find('span', class_="a-offscreen"):
		price = cardElement.find('span', attrs={"class":"a-price", "data-a-color":"price"}).find('span', class_="a-offscreen").text
		cardObj['price'] = price[0]+' '+price[1:]

	''' AMAZON MESSAGES '''
	if cardElement.find('div', class_="a-row a-size-base a-color-secondary s-align-children-center"):
		''' DELIVERY DATE '''
		if cardElement.find('span', attrs={"aria-label":re.compile(r"^Get it by")}):
			cardObj['amazon_message'].append(cardElement.find('span', attrs={"aria-label":re.compile(r"^Get it by")}).get('aria-label'))
		''' FREE DELIVERY '''
		if cardElement.find('span', attrs={"aria-label":re.compile(r"Amazon$")}):
			cardObj['amazon_message'].append(cardElement.find('span', attrs={"aria-label":re.compile(r"Amazon$")}).get('aria-label'))

	''' IMAGES '''
	if cardElement.find('img', attrs={"class":"s-image", "alt":re.compile(r"\w+ (\w+\(\w+\))*")}):
		cardObj['mainImageURL'] = cardElement.find('img', attrs={"class":"s-image", "alt":re.compile(r"\w+ (\w+\(\w+\))*")}).get('src')
		cardObj['imageURLs'] = cardElement.find('img', attrs={"class":"s-image", "alt":re.compile(r"\w+ (\w+\(\w+\))*")}).get('srcset').split(',')
	
	return cardObj

def ListOfCardObjects(soup, domain):
	searchResList = [];
	if soup.find(id="search").find_all(attrs={'data-index':re.compile(r"[1-9]+"), 'data-asin':re.compile(r"\w{8,12}")}):
		cards = soup.find(id="search").find_all(attrs={'data-index':re.compile(r"\d+"), 'data-asin':re.compile(r"\w{6,10}")})
		for card in cards:
			searchResList.append(ExtractFromCard(card, domain))
		
	else:
		print("[UTIL] ListOfCardObjects search error")

	return searchResList


def SearchDomainForKeyword(domain, keyword, limit=None, page=1):
	# print("========== SearchDomainForKeyword ==========")

	from bs4 import BeautifulSoup;
	import urllib.request as Request;
	
	url = "https://{}/s?k={}&page={}".format(domain, keyword, page)

	opener = Request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]

	soup = BeautifulSoup(opener.open(url).read(), 'html.parser')
	print("[UTIL] Fetched search results for {}".format(keyword))

	searchResList = ListOfCardObjects(copy.copy(soup), domain)
	print("[UTIL] {} results obtained from search".format(len(searchResList)))
	
	if limit:
		if len(searchResList) < limit:
			another = SearchDomainForKeyword(domain, keyword, limit=limit-len(searchResList), page=page+1)
			return searchResList + another
		else:
			return searchResList[0:limit]
	else:
		return searchResList

'''
NOTES:
Each card = <div class=s-include-content-margin s-border-bottom s-latency-cf-section>
Mini cards = <div class=s-expand-height s-include-content-margin s-border-bottom s-latency-cf-section>
'''