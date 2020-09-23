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
from classes.amazon import Amazon

instance = Amazon()
print(instance.ProductDetails(PRODUCT_URL)
```