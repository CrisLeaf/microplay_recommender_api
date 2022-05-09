# Microplay Recommender API

A scraper which get all products data from the
[Microplay webpage](https://www.microplay.cl/)

## Requirements

The project was developed in a Python 3.9 environment using the following libraries:

1. [Scrapy](https://scrapy.org/)
2. [Selenium](https://www.selenium.dev/)


## Installation

- Environment Preparation

In a Python 3.9 environment issue

```
pip install Scrapy
pip install selenium
```

- Chrome driver installation

We must install the browser that Selenium will use for the simulations. To use Chrome, install it
in the following link:

https://www.google.com/chrome/

And install the Chrome driver in the link:

https://chromedriver.chromium.org/

## How to run

To run the scraper, on terminal type

```
cd scraper/
scrapy crawl microplay -O data.csv
```


## Support

Give a :star: if you like it :hugs:.
