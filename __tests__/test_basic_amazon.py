import os, sys; sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from classes.Amazon import Amazon

def testInit():
	a = Amazon("https://amazon.in/dp/B078BNQ318")
	assert a != None

def testProductDetails():
	a = Amazon()
	result = a.ProductDetails("https://amazon.in/dp/B078BNQ318")
	assert result.__class__.__name__ == 'dict' and len(result) > 1

def testProductDetailsAsFile():
	a = Amazon()
	result = a.ProductDetailsAsFile("https://amazon.in/dp/B078BNQ318")
	assert result == True

def testKeywordSearch():
	a = Amazon()
	result = a.KeywordSearch("OnePlus", "https://www.amazon.in/")
	assert result != None and result.__class__.__name__ == 'list' and len(result) > 1