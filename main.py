from pprint import pprint
from fake_headers import Headers
import requests
import bs4

base_url="https://habr.com/"
url_salt="ru/all/"
composed_url=base_url+url_salt

lookup_list=["Разработка", "разработка", "Блог", "блог", "Опыт", "опыт"]

header = Headers(browser="chrome", os="win", headers=True).generate()
text = requests.get(composed_url, headers=header).text

soup=bs4.BeautifulSoup(text, features="html.parser")
all_full_snippet=soup.find_all(class_="tm-article-snippet")

#Scraping Date
sep=","
date_list = []
for snippet in all_full_snippet:
    dirty_date=snippet.find_all(class_="tm-article-snippet__datetime-published")
    for date_element in dirty_date:
        date_tag = date_element.find("time")
        normal_date = date_tag.attrs
        date_list.append(normal_date['title'].split(sep,1)[0])

#Scraping Header and Link
headers_list=[]
links_list=[]
for header in all_full_snippet:
    dirty_header=header.find_all("h2")
    for cleaning_header in dirty_header:
        header=cleaning_header.text
        headers_list.append(header)
        dirty_link=cleaning_header.find("a")
        links_list.append(dirty_link['href'])

#Scraping Preview_text
texts_list=[]
for snippet in all_full_snippet:
    dirty_text=snippet.find(class_="article-formatted-body").text
    texts_list.append(dirty_text)

for item in lookup_list:
    for text in texts_list:
        if item in text:
            index = texts_list.index(text)
            print(f"Результат по слову {item} {date_list[index]} - {headers_list[index]} - {base_url}{links_list[index]}")
