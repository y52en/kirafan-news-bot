import requests
import re
from bs4 import BeautifulSoup

# link -> css
# script[src] -> js
# img -> img


def getStr(regex, cssSelector, html):
    return [re.search(regex, str(link))[1] for link in html.select(cssSelector)]


baseurl = "https://kirara.star-api.com"
urls = ["/cat_news/information/", "/cat_news/maintenance/", "/cat_news/update/"]
page1HTML = requests.get(baseurl + urls[0])

parsed = BeautifulSoup(page1HTML.text, "html.parser")

pagelinks = parsed.select(".page-numbers")
oldestPage_href = pagelinks[len(pagelinks) - 1].get("href")
oldestPage = re.search(r"=(\d+)$", oldestPage_href).group(1)

pageTitles = [url.get_text() for url in parsed.find_all("dd")]
pageURLs = getStr(r"Unity\.call\('([^?]+)\?auser_id=", ".newsPost > a", parsed)

new_pageTitles = getStr(r">([^<]+)<", ".new > a > dl > dd", parsed)
new_pageURLs = getStr(r"Unity\.call\('([^?]+)\?auser_id=", ".new > a", parsed)

js_link = getStr(r'"([^"]+)"', "script[src]", parsed)
css_link = getStr(r'"([^"]+)"', "link", parsed)

print(js_link)