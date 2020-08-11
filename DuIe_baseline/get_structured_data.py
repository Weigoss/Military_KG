import sys
sys.path.append('../')

from Crawler import military_crawl as mc
def main():
    # 抓取中华网武器库
    path = '/Users/jas/Desktop/weapon.json'

    weapon = mc.china_crawler(path)
    '''
    weapon.get_page_list()
    weapon.get_link_list()
    weapon.store_text()
    '''
    # weapon.to_KG('kg.json')


if __name__ == "__main__":
    main()