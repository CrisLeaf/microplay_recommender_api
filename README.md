# Microplay Recommender API

A microplay recommendation system api. We used
[Microplay webpage](https://www.microplay.cl/) data, to builda a recommendation system. It was developed using Flask.

## Requirements

To install the required libraries, on terminal run:

```
pip install -r requirements.txt
```

## Data

The data was downloaded from [microplay](https://www.microplay.cl), using Scrapy, Selenium and Chrome web driver.

## How to use

First, one need to train the recommender model. Calling:

`
https://microplay-api.herokuapp.com/train
`

Next, look for any microplay product and add 'reco?url=' to the call. For example:

`
https://microplay-api.herokuapp.com/reco?url=https://www.microplay.cl/producto/mouse-gamer-rgb-griffin-m607w-blanco-redragon/
`

You would get the following:

![](https://raw.githubusercontent.com/CrisLeaf/microplay_recommender_api/main/index.jpeg)

Where the green data is the queried product, and the red ones are the recommended products.


## Tests

To test the recommendation system on terminal run:

```
pytest test_app.py
```



## Support

Give a :star: if you like it :hugs:.
