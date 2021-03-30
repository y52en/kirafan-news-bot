import requests
import re
from bs4 import BeautifulSoup
import archive
import tweet
import saveNews
import os
import copy
from twitter_text import parse_tweet

# tweet.tweet("test")
# link -> css
# script[src] -> js
# img -> img


def getStr(regex, cssSelector, html):
    return [re.search(regex, str(link))[1] for link in html.select(cssSelector)]


host = "https://kirara.star-api.com"
baseurl = "https://kirara.star-api.com/cat_news/"

urls = ["information/", "maintenance/", "update/"]

for url_i, url in enumerate(urls):
    page1HTML = requests.get(baseurl + url)

    parsed = BeautifulSoup(page1HTML.text, "html.parser")

    pagelinks = parsed.select(".page-numbers")
    oldestPage_href = pagelinks[len(pagelinks) - 1].get("href")
    oldestPage = re.search(r"=(\d+)$", oldestPage_href).group(1)

    for pageID in range(1, int(oldestPage) + 1):
        print(str(pageID))
        HTML = requests.get(baseurl + url + "?page=" + str(pageID))

        parsed = BeautifulSoup(HTML.text, "html.parser")

        pageTitles = [url.get_text() for url in parsed.find_all("dd")]
        pageURLs = getStr(r"Unity\.call\('([^?]+)\?auser_id=", ".newsPost > a", parsed)

        new_pageTitles = getStr(r">([^<]+)<", ".new > a > dl > dd", parsed)
        new_pageURLs = getStr(r"Unity\.call\('([^?]+)\?auser_id=", ".new > a", parsed)

        js_link = getStr(r'"([^?"]+)', "script[src]", parsed)
        css_link = getStr(r'"([^?"]+)', "link", parsed)

        if len(new_pageURLs) != 0:
            tmp_title = []
            tmp_url = []

            f = open(
                os.path.expanduser(
                    "~/kirafan-news/" + "tweeted_" + url.replace("/", "") + ".txt"
                ),
                mode="a",
            )

            f_read = open(
                os.path.expanduser(
                    "~/kirafan-news/" + "tweeted_" + url.replace("/", "") + ".txt"
                ),
                mode="r",
            )

            tweeted_ls = [s.replace("\n", "") for s in f_read.readlines()]

            for i, title in enumerate(new_pageTitles):
                if title not in tweeted_ls:
                    tmp_title.append(title)
                    tmp_url.append(new_pageURLs[i])

            for title in tmp_title:
                f.write(title + "\n")

            if len(tmp_title) != 0:
                tweet_str = "新しい"
                if url_i == 1:
                    tweet_str += "メンテナンスの"
                elif url_i == 2:
                    tweet_str += "アップデートの"
                tweet_str += "お知らせがあります\n"

                while len(tmp_title) != 0:
                    tmp_str = tweet_str

                    tmp_str += tmp_title[0]
                    tmp_str += "\n"
                    tmp_str += tmp_url[0]
                    tmp_str += "\n"

                    if parse_tweet(tmp_str).weightedLength > 280:
                        print(tweet_str)
                        tweet.tweet(tweet_str)
                        tweet_str = "続き\n"
                    else:
                        tweet_str = tmp_str
                        tmp_title.pop(0)
                        tmp_url.pop(0)
                print(tweet_str)
                tweet.tweet(tweet_str)
            f.close()

        for js in js_link:
            archive.archiveFile(host + js, "js", "", host)

        for css in css_link:
            archive.archiveFile(host + css, "css", "", host)

        for i, link in enumerate(new_pageURLs):
            # for i, link in enumerate(pageURLs):
            print(link)
            folder = (
                re.search(r"\/(\d+)\/$", link)[1]
                + "_"
                + new_pageTitles[i].replace("/", "／")
            )
            # folder = (re.search(r"\/(\d+)\/$", link)[1] + "_" + pageTitles[i]).replace(
            #     "/", "／"
            # )
            os.makedirs(
                os.path.expanduser("~/kirafan-news/news/" + url + folder), exist_ok=True
            )
            archive.archiveFile(link, "html", url + folder, host)
            saveNews.saveNews(link, url, folder)

        if len(pageTitles) != len(new_pageTitles):
            break


print("fin")
