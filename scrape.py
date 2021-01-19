# import requests;
# import pprint;
# from bs4 import BeautifulSoup;


# URL = 'https://www.monster.com/jobs/search/?q=Software-Developer&where=Australia'
# page = requests.get(URL)

# soup = BeautifulSoup(page.content, 'html.parser')

# results = soup.find(class_='aktuale-single-v4')


# print(results.prettify())


import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

#r = requests.get('https://telegrafi.com/zgjedhjet-2021/')
driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver = webdriver.Chrome()
driver.get("https://telegrafi.com/zgjedhjet-2021/")
button = driver.find_element_by_class_name('btn-meshumeLajme')
button.click()

time.sleep(1)

soup = BeautifulSoup(driver.page_source, 'html.parser')

stories = []
linksArray = []
vv = 0
pdk = 0
aak = 0
nisma = 0
kurti = 0

data = soup.findAll('div',attrs={'class':'aktuale-widget'})
for div in data:
    links = div.findAll('a')
    for a in links:
        if a.get('href'):
            linksArray.append(a.get('href'))

while(len(linksArray) > 30):
    del linksArray[-1]
print(len(linksArray))
print(linksArray)

for link in linksArray:
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = soup.findAll('div',attrs={'class':'article-body'})
    for div in data:
        paragraphs = div.findAll('p')
        for p in paragraphs:
            text = p.text.lower()
            if "vv" in text:
                vv+= 1
            if "pdk" in text:
                pdk+= 1
            if "aak" in text:
                aak+= 1
            if "nisma" in text:
                nisma+= 1
            if "kurti" in text:
                kurti+= 1

print(vv, pdk, aak, nisma, kurti)
#print(linksArray);
[u'Using Binary Diffing to Discover Windows Kernel Memory Disclosure Bugs', 'https://googleprojectzero.blogspot.com/2017/10/using-binary-diffing-to-discover.html']