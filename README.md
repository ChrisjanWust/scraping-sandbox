# scraping-sandbox

### Requirements

Python 3.6+

Only module required is `scrapy`. I'm specifically running v1.5.1 - anything newer should be fine.

### Run

```
scrapy crawl makro
```

### Splash

Splash is essentially a headless browser. The reason it's required is for it's Javascript rendering, as Scrapy directly uses the raw result of an HTTP request. JS rendering isn't needed for all sites, but some only render critical information with the JS. It is preferred to use as little SplashRequests as possible because of the increased computation (so on some sites, like Takealot)

##### Setup

The install setup for Splash is documented here: <https://splash.readthedocs.io/en/latest/install.html>

It's quite simple. First pull the docker container:

```
docker pull scrapinghub/splash
```

Note that you might need to add a `sudo` for Linux.

To run the container:

```
docker run -it -p 8050:8050 --rm scrapinghub/splash
```

Now Splash is available as a headless browser on `localhost:8050`.

##### Use with Scrapy

Splash has a direct replacement for a `scrapy.Request`, `SplashRequest`:

```
yield SplashRequest(
	url,
	self.parse_result,
    args={  # optional; parameters passed to Splash HTTP API
        'wait': 0.5,
    },
)
```

To use this, a few settings need to be set as defined here: <https://github.com/scrapy-plugins/scrapy-splash#usage>

These (except for caching) have already been done in `splash_settings.json`.

We pull them in using

```
with open('scrapers/splash_settings.json') as f:
    splash_settings = json.load(f)
custom_settings = {**custom_settings, **splash_settings
```

See the *Takealot* spider as example.