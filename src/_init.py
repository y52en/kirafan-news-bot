import os


def mkdirs(path):
    os.makedirs(os.path.expanduser(path), exist_ok=True)


mkdirs("~/kirafan-news/assets/js")
mkdirs("~/kirafan-news/assets/css")
mkdirs("~/kirafan-news/assets/img")
mkdirs("~/kirafan-news/news/information")
mkdirs("~/kirafan-news/news/maintenance")
mkdirs("~/kirafan-news/news/update")