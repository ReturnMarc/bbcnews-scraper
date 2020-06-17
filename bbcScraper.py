import requests
from bs4 import BeautifulSoup
import json

root_url = 'https://www.bbc.com'
response = requests.get(root_url+"/news")
doc = BeautifulSoup(response.text, 'html.parser')

def findBBCArticle(url):
    print(url)
    responseArticle = requests.get(url)
    soup = BeautifulSoup(responseArticle.text, 'html.parser')
    
    body = soup.find(property="articleBody")
    description = [p.text for p in body.find_all("p")]
    if description:
        description = '\n'.join(description)
    
    try : 
        imgUrl = soup.find('img',{'class':"js-image-replace"}).get('src')
        #if imgUrl:
        #    print(imgUrl)
    except:
        print("No Image")
    #imgUrl = 'test'
    
    time = soup.find(class_="date").attrs['data-seconds']
    
    
    #if time:
    #    print(time)
    #time = "fdsdf"
    return description,imgUrl,time

def BBCScraper():
    
    news_list = []
    newsAll = doc.find_all('div', { 'class': 'gs-c-promo' })
    for news in newsAll:
        headline = news.find('h3')
        link = news.find('a')


        articleUrl = root_url+link['href']



        try:
            description,imgUrl,time = findBBCArticle(articleUrl)
            
            
            article = {
                  "source": {
                    "id": link['href'],
                    "name": "BBC"
                    },
                    "author": "Null",
                    "title": headline.text,
                    "description": description,
                    "url": articleUrl,
                    "urlToImage": imgUrl,
                    "publishedAt": time
                }
            
            # Add the dict to our list
            news_list.append(article)

        except:
            print("Url error")



    #print(stories_list)


    with open('bbcNews.json', 'w', encoding='utf-8') as file:
        json.dump(news_list , file, ensure_ascii=False, indent=4)

    

BBCScraper()
