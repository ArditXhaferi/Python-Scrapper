import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json


# def scrape_site_telegrafi():
#     driver = webdriver.Chrome(executable_path='./chromedriver.exe')
#     driver = webdriver.Chrome()
#     driver.get("https://telegrafi.com/zgjedhjet-2021/")
#     button = driver.find_element_by_class_name('btn-meshumeLajme')
#     button.click()

#     time.sleep(1)

#     soup = BeautifulSoup(driver.page_source, 'html.parser')

#     linksArray = []
#     keywordsArray = ["pdk", "aak", "kurti", "parti"]
#     keywordsCount = {}
#     dataObject = {}
#     for keyword in keywordsArray:
#         dataObject[keyword] = {}

#     data = soup.findAll('div',attrs={'class':'aktuale-widget'})
#     for div in data:
#         links = div.findAll('a')
#         for a in links:
#             if a.get('href'):
#                 linksArray.append(a.get('href'))

#     while(len(linksArray) > 30):
#         del linksArray[-1]

#     for link in linksArray:
#         r = requests.get(link)
#         soup = BeautifulSoup(r.text, 'html.parser')
#         data = soup.find('div',attrs={'class':'article-body'})
#         for keyword in keywordsArray:
#             keywordsCount[keyword] = 0
#         text = data.text.lower()
#         for keyword in keywordsArray:
#             keywordsCount[keyword] += text.count(keyword)
#         for keyword in keywordsArray:
#             if keywordsCount[keyword] != 0:
#                 dataObject[keyword][link] = keywordsCount[keyword]

#     print(dataObject)

# scrape_site_telegrafi()

# r = requests.get('https://kosovapress.com/lajme/')

# soup = BeautifulSoup(r.content, 'html.parser')

# linksArray = []
# keywordsArray = ["pdk", "aak", "kurti", "parti"]
# keywordsCount = {}
# dataObject = {}
# for keyword in keywordsArray:
#     dataObject[keyword] = {}

# links = soup.findAll('a',attrs={'class':'img-opacity-hover'})

# for a in links:
#     if a.get('href'):
#         linksArray.append(a.get('href'))

# while(len(linksArray) > 30):
#     del linksArray[-1]

# for link in linksArray:
#     r = requests.get(link)
#     soup = BeautifulSoup(r.text, 'html.parser')
#     data = soup.find('div',attrs={'class':'entry-content'})
#     for keyword in keywordsArray:
#         keywordsCount[keyword] = 0
#     text = data.text.lower()
#     for keyword in keywordsArray:
#         keywordsCount[keyword] += text.count(keyword)
#     for keyword in keywordsArray:
#         if keywordsCount[keyword] != 0:
#             dataObject[keyword][link] = keywordsCount[keyword]

# print(dataObject)
dataObject = {}
sites = ["Kosovapress", "Telegrafi", "GazetaExpress", "Koha", "Indeksonline", "BotaSot", "Reporteri", "Insajderi"]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}
for site in sites:
    dataObject[site] = {}

def scrape_site(click, url, element, link_dom, text_dom, site, button):
    if click:
        driver = webdriver.Chrome(executable_path='./chromedriver.exe')
        driver = webdriver.Chrome()
        driver.get(url)
        button = driver.find_element_by_class_name(button)
        button.click()
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    else:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

    linksArray = []
    keywordsArray = ["pdk", "vv", "ldk", "nisma"]
    keywordsCount = {}
    for keyword in keywordsArray:
        dataObject[site][keyword] = {}
    if element == "a":
        links = soup.findAll(element, attrs={'class': link_dom})
        for a in links:
            if a.get('href'):
                linksArray.append(a.get('href'))
    else:
        data = soup.findAll(element, attrs={'class': link_dom})
        for div in data:
            links = div.findAll('a')
            for link in links:
                if link.get('href'):
                    if site == "Koha":
                        linksArray.append("https://www.koha.net" + link.get('href'))
                    elif site == "BotaSot":
                        linksArray.append("https://www.botasot.info/" + link.get('href'))
                    else:
                        linksArray.append(link.get('href'))
    for link in linksArray:
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        content = soup.find('div', attrs={'class': text_dom})
        for keyword in keywordsArray:
            keywordsCount[keyword] = 0
        text = content.text.lower()
        for keyword in keywordsArray:
            keywordsCount[keyword] += text.count(keyword)
        for keyword in keywordsArray:
            if keywordsCount[keyword] != 0:
                dataObject[site][keyword][link] = keywordsCount[keyword]
scrape_site(bool(0), 'https://kosovapress.com/lajme/', "a", "img-opacity-hover", "entry-content", "Kosovapress", "")
scrape_site(bool(1), 'https://telegrafi.com/zgjedhjet-2021/', "div", "aktuale-widget", "article-body", "Telegrafi", "btn-meshumeLajme")
scrape_site(bool(0), 'https://www.gazetaexpress.com/zgjedhjet2021/', "a", "right-post-category", "single__content", "GazetaExpress", "")
scrape_site(bool(0), 'https://www.koha.net/tag/zgjedhjet-2021/', "div", "row clear mgb-30", "news-content", "Koha", "")
scrape_site(bool(1), 'https://indeksonline.net/zgjedhjet/', "li", "box_style_paginated", "article-content", "Indeksonline", "loadmore-inf")
scrape_site(bool(0), 'https://www.botasot.info/lajme/', "div", "related-down", "main-paragraph", "BotaSot", "")
scrape_site(bool(0), 'https://reporteri.net/zgjedhjet2021/', "div", "td-module-thumb", "td-post-content", "Reporteri", "")
scrape_site(bool(0), 'https://insajderi.com/lajme/', "div", "lajme_c", "text-holder", "Insajderi", "")

with open('data.json', 'w') as outfile:
    json.dump(dataObject, outfile)
print(dataObject)