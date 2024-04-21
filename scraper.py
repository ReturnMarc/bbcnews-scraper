import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime


def load_sport_categories():
    root_url = 'https://www.bbc.com/sport/all-sports'
    response = requests.get(root_url)
    doc = BeautifulSoup(response.text, 'html.parser')
    liste_cat = []

    links = doc.find_all('a')
    for link in links:
        liste_cat.append(link.get('href'))


    categories_links = [link for link in liste_cat if '/sport' in link]
    categories_links = [link for link in categories_links if 'https://www.bbc.com' not in link]
    categories_links = [link for link in categories_links if 'https://www.bbc.co.uk' not in link]
    categories_links = categories_links[3:-7]
    categories_links = ["/".join(link.split('/')[2:]) for link in categories_links]
    categories_links = list(set(categories_links))

    with open('sport_categories.csv', mode='w', newline='', encoding='utf-8') as datei:
        csv_writer = csv.writer(datei)
        for element in categories_links:
            csv_writer.writerow([element])

# load_sport_categories() # Uncomment to run. Only run if you really want to reload the categories, from bbc directly. This should only be necessary if the categories on the website change.

def get_sport_categories(filename: str):
    categories = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
    
        for row in reader:
            categories.append(row[0])

    return set(categories)


categories = get_sport_categories('sport_categories.csv')
root_url = 'https://www.bbc.com/sport'
modified_url = root_url[:root_url.rfind("/")] # remove last part of url, because articles in sport dont have full url
text_list = []

for category in categories:
    list_url = set()
    response = requests.get(root_url + r"/" + category)
    doc = BeautifulSoup(response.text, 'html.parser')
    newsAll = doc.find_all('div', { 'class':"ssrcss-1f3bvyz-Stack e1y4nx260" }) # find all news articles on the selected sport category page


    for news in newsAll:
        try:
            article_path = news.find('a') # find url of the article in article class
            if article_path['href'].startswith('/sport'): #filter out links that are not articles
                article_url = modified_url + article_path['href']
                list_url.add(article_url)
            else:
                continue

        except TypeError: # if no url is found
            continue


    for article_url in list_url:
        article = {}
        response = requests.get(article_url)
        doc = BeautifulSoup(response.text, 'html.parser')

        article['url'] = article_url
        article['category'] = category

        # get article heading
        # heading = doc.find('h1', {'id':"main-heading"})
        heading = doc.find('h1')
        try:
            article['heading'] = heading.text # type: ignore
        except AttributeError: # if no heading is found
            article['heading'] = '0'

        # get article publication date
        publication_date = doc.find('time')
        try:
            article['publication_date'] = publication_date['datetime'] # type: ignore
        except TypeError: # if no publication date is found
            article['publication_date'] = '0'

        # get article description
        if category == 'football':
            description = doc.find('p', {'role':'introduction'})
        else:
            description = doc.find('b', {'class':"ssrcss-1xjjfut-BoldText e5tfeyi3"})

        try: 
            article['description'] = description.text # type: ignore
        except AttributeError: # if no description is found
            article['description'] = '0'

    # get article text
        article_text = str()
        if category == 'football':
    
            textAll = doc.find_all('article')
            for text in textAll:
                paragraphs = text.find_all('p')
                for paragraph in paragraphs:
                    article_text = article_text + " " + paragraph.text
        else:

            textAll = doc.find_all('div',{'class':"ssrcss-7uxr49-RichTextContainer e5tfeyi1"})
            for text in textAll:
                paragraphs = text.find_all('p', { "class":"ssrcss-1q0x1qg-Paragraph e1jhz7w10" })
                for paragraph in paragraphs:
                    article_text = article_text + " " + paragraph.text

        article['text'] = article_text

        text_list.append(article)
        print('Article added: ', article['heading'])

# Remove empty articles
text_list_clean = [article for article in text_list if article['text'] != ""]

print('No of articles found: ',len(text_list_clean))

# Write to json file
now = datetime.now().date()

with open(str(now) + '_bbc_sport.json', 'w', encoding='utf-8') as json_file:
    json.dump(text_list_clean, json_file, indent=4)