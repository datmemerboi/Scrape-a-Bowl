from bs4 import BeautifulSoup; import os, copy; import json as JSON;

def CreateProductObject(soup, url):
	productObj = { 'url':url, 'imageURLs':[], 'features':[], 'description':{}, 'specs':[], 'variations':[] }

	''' TITLE '''
	if soup.find(id="productTitle"):
		productObj['title'] = soup.find(id="productTitle").text.strip("\n").strip()
		productObj['name'] = soup.find(id="productTitle").text.strip("\n").strip()

	''' DESCRIPTION '''
	if(soup.find(id="productDescription")):
		for child in soup.find(id="productDescription").children:
			if child.__class__.__name__ == "Tag":
				if child.name == "div" and 'disclaim' in child['class']:
					productObj['description']['variant'] = child.strong.text
				else:
					productObj['description']['text'] = child.text.strip('').strip('\n')

	''' BYLINEINFO '''
	if soup.find(id="bylineInfo"):
		productObj['seller'] = soup.find(id="bylineInfo").text

	''' PRICE '''
	if soup.find(id="priceblock_ourprice"):
		productObj['price'] = soup.find(id="priceblock_ourprice").text.replace('\xa0', ' ')

	''' TWISTER FORM '''
	# print(soup.find(id="twister").contents[3])

	''' FEATURES '''
	if soup.find(id="feature-bullets").find_all('span', class_="a-list-item"):
		for featureItem in soup.find(id="feature-bullets").find_all('span', class_="a-list-item"):
			productObj['features'].append(featureItem.text.strip().strip('\n'))

	''' SPECS '''
	keys = [key.text.strip('\n').strip() for key in soup.find_all("td", class_="label")]
	vals = [val.text.strip('\n').strip() for val in soup.find_all("td", class_="value")]

	labels = ["label"] * len(keys); values = ["value"] * len(vals);

	productObj['specs'].extend(\
		list(\
			map(\
				lambda labKey, valVal: {labKey[0]:labKey[1], valVal[0]:valVal[1]},\
				list( zip(labels, keys) ), list( zip(values, vals) )\
			)
		)
	)

	''' DATE '''
	if productObj['specs']:
		productObj['date'] = list(filter(lambda featureObj: 'Date First Available' in featureObj['label'], productObj['specs']))[0]['value']

	''' ASIN '''
	if productObj['specs']:
		productObj['ASIN'] = list(filter(lambda featureObj: 'ASIN' in featureObj['label'], productObj['specs']))[0]['value']

	# ''' CUSTOMER RATING '''
	if 'out of' in soup.find(id='reviewsMedley').find_all('span', class_="a-size-medium a-color-base")[0].text:
		productObj['customer_rating'] = soup.find(id='reviewsMedley').find_all('span', class_="a-size-medium a-color-base")[0].text.replace('\n', '').strip()

	if 'customer rating' in soup.find(id='reviewsMedley').find_all('span', class_="a-size-base a-color-secondary")[0].text:
		string = soup.find(id='reviewsMedley').find_all('span', class_="a-size-base a-color-secondary")[0].text.replace(',', '')
		productObj['customer_rating_count'] = int( list( filter( lambda x: x.isdigit(), string.split() ) )[0] )

	''' MAIN IMAGE URL '''
	if soup.find(id='altImages').find_all('span', class_="a-button-text"):
		productObj['mainImageURL'] = soup.find(id='altImages').find_all('span', class_="a-button-text")[0].find_all('img')[0].get('src')

	''' OTHER IMAGES '''
	if soup.find(id='altImages').find_all('span', class_="a-button-text"):
		for imgSpan in soup.find(id='altImages').find_all('span', class_="a-button-text"):
			productObj['imageURLs'].append(imgSpan.find('img').get('src')) if imgSpan.find('img') else None

	''' VARIATION '''

	def getTitleValuesOfID(soup, ID, key):
		i = 0; ret = [];
		while soup.find(id = ID+str(i)):
			val = soup.find(id = ID+str(i)).get('title').replace('Click to select ', '')
			ret.append("{}: {}".format(key, val))
			i+=1
		return ret

	if(soup.find(id="variation_style_name")):
		productObj['variations'].extend(getTitleValuesOfID(copy.copy(soup), "style_name_", "Style"))

	if(soup.find(id="variation_size_name")):
		productObj['variations'].extend(getTitleValuesOfID(copy.copy(soup), "size_name_", "Size"))

	if(soup.find(id="variation_color_name")):
		productObj['variations'].extend(getTitleValuesOfID(copy.copy(soup), "color_name_", "Colour"))

	print("[UTIL] ProductObject created successfully!")
	return productObj

def ProductUtil(html, url):
	# print("========== ProductUtil ==========")
	try:
		soup = BeautifulSoup(html, 'html.parser')
		return CreateProductObject(copy.copy(soup), url)

	except Exception as err:
		print("[UTIL] ProductUtil error:")
		print(err)
		return False

def ProductFileUtil(htmlFilePath, url):
	# print("========== ProductFileUtil ==========")
	try:
		with open(htmlFilePath, 'r') as file:
			html = file.read()
			file.close()

		soup = BeautifulSoup(html, 'html.parser')
		productObj = CreateProductObject(copy.copy(soup), url)
		
		if not os.path.exists(os.path.join(os.path.dirname(__file__), '..', '..', 'output')):
			os.makedirs(os.path.exists(os.path.join(os.path.dirname(__file__), '..', '..', 'output')))

		with open(os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'output.json'), 'w+') as file:
			JSON.dump(productObj, file)
			print("[UTIL] Written into output/output.json")
			file.close()

		return os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'output.json')

	except Exception as err:
		print("[UTIL] ProductFileUtil error:")
		print(err)
		return False


# ProductFileUtil("/home/dmb/Assignments/URL-JSON-souper/html/current.html", "http://www.amazon.in/dp/B07BDNGTYC")