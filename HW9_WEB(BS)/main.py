import json

import requests
from bs4 import BeautifulSoup
import re

BASE_URL = 'https://quotes.toscrape.com/'
num = 1
urls = ["/"]
urls_authors = []
while True:
    print("Data collection. Pleas wait :)")
    prefix = "page/"
    html_doc = requests.get(BASE_URL + prefix + str(num))
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    content = soup.select("li.next a")
    if content:
        for link in content:
            url = prefix + re.search(r"\d+/", link["href"]).group()
            print(url)
            urls.append(url)
        num += 1
    else:
        break


def quotes_search_save(u):
    response = requests.get(BASE_URL+u)
    s = BeautifulSoup(response.content, 'html.parser')
    quotes = s.find_all('span', class_='text')
    authors = s.find_all('small', class_='author')
    tags = s.find_all('div', class_='tags')
    quotes_list = []
    prefix2 = "author/"
    for i in range(0, len(quotes)):
        quotes_dict = {"quote": quotes[i].text,
                       "author": authors[i].text,
                       "tags": []}
        tags_for_quote = tags[i].find_all('a', class_='tag')
        for tag_for_quote in tags_for_quote:
            quotes_dict["tags"].append(tag_for_quote.text)
        quotes_list.append(quotes_dict)

        urls_authors.append(prefix2 + authors[i].text)
    return quotes_list


def authors_search_save(u):
    response = requests.get(BASE_URL+u)
    s = BeautifulSoup(response.text, 'lxml')
    full_name = s.find_all('h3', class_='author-title')
    born_date = s.find_all('span', class_='author-born-date')
    born_location = s.find_all('span', class_='author-born-location')
    description = s.find_all('div', class_='author-description')
    authors_list = []
    for i in range(0, len(born_location)):
        authors_dict = {"fullname": full_name[i].text,
                        "born_data": born_date[i].text,
                        "born_location": born_location[i].text,
                        "description": str(description[i].text).strip()}
        authors_list.append(authors_dict)
        print(authors_dict)
    return authors_list


def clean_list(li):
    b = []
    for i in li:
        if i not in b:
            b.append(i)
    return b


if __name__ == '__main__':
    quote_save = []
    author_save = []
    clean_urls_authors = []
    for ur in urls:
        quote_save.extend(quotes_search_save(ur))
    cl_li = clean_list(urls_authors)
    print(cl_li)
    for c in cl_li:
        c = str(c).replace(" ", "-").replace("'", "").replace("é", "e").replace(".", "-").replace("--", "-")
        if c.endswith("-"):
            x = c.rfind("-")
            y = c[:x]
            clean_urls_authors.append(y)

        else:
            clean_urls_authors.append(c)
    print(clean_urls_authors)
    for p in clean_urls_authors:
        author_save.extend(authors_search_save(p))
    with open("quotes.json", "w", encoding='utf-8') as fd:
        json.dump(quote_save, fd, ensure_ascii=False, indent=2)

    with open("authors.json", "w", encoding='utf-8') as fd:
        json.dump(author_save, fd, ensure_ascii=False, indent=2)
