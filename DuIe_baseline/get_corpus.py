import sys
sys.path.append('../')

from Crawler import military_crawl as mc


def main():
    """
    type = [website, category]
    website_list = ['sina', 'sohu']
    category_list = ['china', 'international', 'weapon', 'national_defence', 'univerasl']
    """
    # 抓取新浪网中国军情
    path = 'sina_china.csv'
    sina_china = mc.sina_crawler(path, ['sina', 'china'])
    sina_china.get_link_list()
    sina_china.get_text()

    # 抓取新浪网国际军情
    path = 'sina_international.csv'
    sina_inter = mc.sina_crawler(path, ['sina', 'international'])
    sina_inter.get_link_list()
    sina_inter.get_text()


if __name__ == "__main__":
    main()
