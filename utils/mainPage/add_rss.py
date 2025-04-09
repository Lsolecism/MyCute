import feedparser
from bs4 import BeautifulSoup


def add_rss(rssAddress):
    feed = feedparser.parse(rssAddress)
    for entry in feed.entries:
        print(entry.title)
        print(entry.description)
        print(entry.link)
        print(entry.published)
        print(entry.author)
        print(entry.content[0].value)
        soup = BeautifulSoup(entry.content[0].value, "html.parser")
        first_image = soup.find("img")
        # 获取图片的 URL
        if first_image and 'src' in first_image.attrs:
            image_url = first_image['src']
            # 设置第一张图片的url
            entry['image_url'] = image_url
        else:
            entry['image_url']= "https://c-ssl.duitang.com/uploads/blog/202011/16/20201116230615_57a8e.thumb.1000_0.jpg"

    return feed.entries