import urllib.request

url = "https://docs.python.org/2.7/"  # 読み込むファイルのURL
urllib.request.urlretrieve(url, "~/hoge/python.html")