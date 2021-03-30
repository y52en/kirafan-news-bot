import requests
import re
from bs4 import BeautifulSoup
import archive


def getStr(regex, cssSelector, html):
    return [re.search(regex, str(link))[1] for link in html.select(cssSelector)]


baseurl = "https://kirara.star-api.com"


def saveNews(path, url, folder):
    HTML = requests.get(path)
    parsed = BeautifulSoup(HTML.text, "html.parser")

    js_link = getStr(r'"([^?"]+)', "script[src]", parsed)
    css_link = getStr(r'"([^?"]+)', 'link[rel="stylesheet"]', parsed)

    img_link = getStr(r'src="([^?"]+)', "img[src]", parsed)
    assets_link = getStr(r"url\(([^?)]+)", "div[style*='background-image']", parsed)

    for js in js_link:
        archive.archiveFile(js, "js", "", path)

    for css in css_link:
        archive.archiveFile(css, "css", "", path)

    for asset in assets_link:
        archive.archiveFile(asset, "asset", "", path)

    for img in img_link:
        archive.archiveFile(img, "img", url + folder + "/", path)
