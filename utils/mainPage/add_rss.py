import feedparser
from bs4 import BeautifulSoup

from mycutedb.add_method import add_Rss
from mycutedb.get_method import get_user_id


def add_rss(email,rss_name,rssAddress):
    userId = get_user_id(email)
    feed = feedparser.parse(rssAddress)
    print(feed)
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

    add_Rss(userId,rss_name,rssAddress,feed.entries)
    return feed.entries

