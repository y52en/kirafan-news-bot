import urllib.request
import re
import os

# import urllib.parse


def savefile(url, path):
    path = path
    savepath = os.path.expanduser(path)
    if os.path.exists(savepath) is False:
        print(url + "_" + path + "_" + savepath)
        try:
            urllib.request.urlretrieve(url, savepath)
        except urllib.error.URLError:
            try:
                print("retry1")
                urllib.request.urlretrieve(url, savepath)
            except urllib.error.URLError:
                print("retry2")
                urllib.request.urlretrieve(url, savepath)


def archiveFile(url, filetype, savePath, baseUrl):
    noDownloadList = [
        "https://krr-dev-web.star-api.com/wp-content/uploads/2019/09/専用武器追加_201910-1.png",
        "https://krr-dev-web.star-api.com/wp-content/uploads/2019/05/NEW-GAME_-期間限定特別_クロモン.png",
        "http://krr-dev-web.star-api.com/wp-content/uploads/2018/05/Profile_naru_hanayamata1_1_Ud7fKyWG.png",
        "https://krr-dev-web.star-api.com/wp-content/uploads/2018/08/29002000用帯.png",
    ]

    if url in noDownloadList:
        return

    if re.match(r"\/", url):
        host = re.match(r"https:\/\/[^\/]+", baseUrl)[0]
        url = host + url
    # print(url)

    # fileName = ""
    if filetype != "html":
        fileName = re.search(r"\/([^\/]+)$", url)[1]

    if filetype == "js":
        savefile(url, "~/kirafan-news/assets/js/" + fileName)
    elif filetype == "css":
        savefile(url, "~/kirafan-news/assets/css/" + fileName)
    elif filetype == "asset":
        savefile(url, "~/kirafan-news/assets/img/" + fileName)
    elif filetype == "img":
        savefile(url, "~/kirafan-news/news/" + savePath + fileName)
    elif filetype == "html":
        savefile(url, "~/kirafan-news/news/" + savePath + "/index.html")
