# News Scraper
It's BBC news scraper. It can scrape all categories of bbc news with customizable format.

# Requirement
* Python 3

# Example format
```bash
[
    {
        "id": "/news/world-europe-53175459",
        "source": "BBC",
        "type": "politics",
        "author": "Null",
        "title": "'Very significant' Europe resurgences alarm WHO",
        "description": "Europe has seen an increase..........",
        "url": "https://www.bbc.com/news/world-europe-53175459",
        "image_url": "https://ichef.bbci.co.uk/news/320/cpsprodpb/12B7D/production/_113096667_mediaitem113096663.jpg",
        "published_at": "1593097234",
        "updated_at": "1593097234"
    },
    {
        "id": "/news/world-asia-53174887",
        "source": "BBC",
        "type": "politics",
        "author": "Null",
        "title": "Images 'show China structures' on India border",
        "description": "China has built new structures ...................",
        "url": "https://www.bbc.com/news/world-asia-53174887",
        "image_url": "https://ichef.bbci.co.uk/news/320/cpsprodpb/16E35/production/_113094739_galwan_valley_chinese_structures_pic976.jpg",
        "published_at": "1593102731",
        "updated_at": "1593102731"
    },
    ..............    
]

```


## Quick Run
```bash
    git clone git@gitlab.com:codephilics/news-scraper.git

    cd news-scraper

    pip install bs4

    pip install requests

    python bbcScraper.py
```
