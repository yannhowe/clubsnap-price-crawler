# clubsnap-price-crawler
Quick and dirty grab of things for sale on clubsnap. User scrapy and send the output to a postgres DB.

# setup & configuration
You'll need an instand of posgres to funnel all the data to. Mac users can use [this](http://postgresapp.com/) windows users can use [this](https://www.postgresql.org/download/windows/).

Configure ```/camprice/settings.py``` with the postgres settings

Configure URIs to crawl in the spider file ```camprice/camprice/spiders/clubsnap_spider.py```

Run the spider from inside directry ```caprice``` run ```scrapy crawl clubsnap2```

The data should be now be in your postgres DB. Browse it, do stuff with it.
