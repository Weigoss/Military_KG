import sys
sys.path.append('../')

from Crawler import military_crawl as mc

def main():
    """
    # 抓取新浪网中国军情
    url = 'http://mil.news.sina.com.cn/roll/index.d.html?cid=57918&page={}'
    page = 25
    path = '/Users/jas/Desktop/sina_china.csv'
    sina_china = sina_crawler(url, page, path)
    sina_china.get_link_list()
    sina_china.get_text()
    """

    """
    # 抓取新浪网国际军情
    url = 'http://mil.news.sina.com.cn/roll/index.d.html?cid=57919&page={}'
    page = 25
    path = '/Users/jas/Desktop/sina_international.csv'
    sina_inter = sina_crawler(url, page, path)
    sina_inter.get_link_list()
    sina_inter.get_text()
    """

if __name__ == "__main__":
    main()
