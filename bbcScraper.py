import requests
from bs4 import BeautifulSoup
import json

# BBC home page 
root_url = 'https://www.bbc.com'
response = requests.get(root_url + "/news/world")
doc = BeautifulSoup(response.text, 'html.parser')

def find_bbc_article(url):
    print(url)
    # BBC article page
    response_article = requests.get(url)
    soup = BeautifulSoup(response_article.text, 'html.parser')
    
    
    # Find article descrition 
    body = soup.find(property="articleBody")
    description = [p.text for p in body.find_all("p")]
    if description:
        description = '\n'.join(description)
    
    # Find articles image
    try : 
        img_url = soup.find('img',{'class':"js-image-replace"}).get('src')
    except:
        print("No Image")
    
    # Find article time
    time = soup.find(class_="date").attrs['data-seconds']
    
    return description,img_url,time

# All articles list
news_list = []

def bbc_scraper():
     
    # Find all news or articles
    newsAll = doc.find_all('div', { 'class': 'gs-c-promo' })
    
    # Traverse all news or articles
    for news in newsAll:
        headline = news.find('h3')
        article_path = news.find('a')

        article_url = root_url + article_path['href']

        try:
            description,img_url,time = find_bbc_article(article_url)
    
            article = {
                  "source": {
                    "id": article_path['href'],
                    "name": "BBC"
                    },
                    "author": "Null",
                    "title": headline.text,
                    "description": description,
                    "url": article_url,
                    "urlToImage": img_url,
                    "publishedAt": time
                }

            # Add the article to our list
            news_list.append(article)
        except:
            print("Url error")


catagories = ["","/world","/asia","/uk","/business","/technology"]#,"/science_and_environment","/entertainment_and_arts","/health"]
for catagory in catagories:
    response = requests.get(root_url + "/news"+catagory)
    doc = BeautifulSoup(response.text, 'html.parser')
    bbc_scraper()

print("Total news:",len(news_list))

with open('bbcNews.json', 'w', encoding='utf-8') as file:
        json.dump(news_list , file, ensure_ascii=False, indent=4)


