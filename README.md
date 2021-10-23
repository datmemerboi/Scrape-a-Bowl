Scrape A Bowl
=
## Python | BeautifulSoup

Python project to Scrape web for products & reviews.

Currently functional for Amazon (.in, .com, .co.uk)

_Feel free to test other domains and report issues_

### Installation
Run `pip install -r requirements.txt`.

### First Run
```
import json
from classes import Amazon
instance = Amazon()

# Extracting single product data
print(instance.ProductDetails(SOME_PRODUCT_URL)

# Searching for a keyword
print(instance.KeywordSearch(SOME_KEYWORD, "amazon.in"))
```