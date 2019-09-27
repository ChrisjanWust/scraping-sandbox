# scraping-sandbox

### Requirements

Only requirement is `scrapy`. I'm specifically running v1.5.1 - anything newer should be fine.

### Run

```
scrapy crawl makro
```

### Task

Write a scraper for [Hirschs](hirschs.co.za) using a similar format to that of the Makro scraper.

The output should be a list of item dictionaries, such as:

```
{
  "model_nr": "58A6100UW",
  "brand": "HISENSE",
  "name": " HISENSE   146 cm (58\")   Smart UHD TV ",
  "url": "https://www.makro.co.za/electronics-computers/televisions/led/-46-117cm-/hisense-146-cm-58-smart-uhd-tv-/p/000000000000370254_EA",
  "specs": {
    "Screen Type": "UHD",
    "3D": "-",
    "Resolution": "3480 x 2160",
    "Smart": "Yes",
    "Clear Motion Ratio(H": "-",
    "HDMI Inputs": "3",
    "USB Inputs": "2",
    "Contrast Ratio": "4000:1",
    "Smart Interactive": "Yes",
    "Wi-Fi Ready": "Yes",
    "Wireless Lan Built I": "Yes",
    "Bluetooth Technology": "-",
    "Internet Ready": "Yes",
    "Skype Ready": "-",
    "Dongle Included": "-",
    "Built In Camera": "-",
    "Built In Microphone": "-",
    "3D Glasses Included": "-",
    "Remotes Included": "Yes",
    "TV Dim With Stand": "1301 x 244 x 821",
    "TV Dim W/out Stand": "1301 x 74 x 760",
    "gtin": "6942147447888"
  },
  "image_url": "https://www.makro.co.za/sys-master/images/h32/h9f/8904066990110/silo-MIN_370254_EAA_large",
  "category": [
    "Home",
    "Electronics & Computers",
    "Televisions",
    "LED",
    "> 46\" (117cm)"],
  "pricing_data": {
    "supplier": "Makro",
    "sku": "000000000000370254_EA",
    "price": "7999.00"
  }
}
```

The data isn't fully cleaned yet, which is fine. The goal, for now, is just to get structured data for further local parsing.

