from bs4 import BeautifulSoup
import re
import time
import json
import requests
import csv

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

website_list = ['sina', 'sohu']
category_list = ['china', 'international', 'weapon', 'national_defence', 'univerasl']


class sina_crawler(object):
    """
    爬取新浪网军事报道文章
    """

    def __init__(self, path, type=['sina', 'china']):
        # 储存页面url
        self.page_list = []
        # 储存文章url
        self.link_list = []
        self.path = path
        self.type = type
        if type[0] not in website_list or type[1] not in category_list:
            raise ValueError
        if type[0] == 'sina':
            if type[1] == 'china':
                url = 'http://mil.news.sina.com.cn/roll/index.d.html?cid=57918&page={}'
                page = 25
            elif type[1] == 'international':
                url = 'http://mil.news.sina.com.cn/roll/index.d.html?cid=57919&page={}'
                page = 24
            else:
                raise ValueError
        for i in range(1, page + 1):
            self.page_list.append(url.format(i))

    def get_link_list(self):
        # 获取文章链接
        for url in self.page_list:
            response = requests.get(url=url, headers=headers)
            response.encoding = 'UTF-8'
            html = BeautifulSoup(response.text, "html.parser")
            for linkNews in html.find_all('ul', class_="linkNews", style=False):
                # 文章发布时间
                date = linkNews.find('span').text
                date = date.strip('(').strip(')').strip()
                # day_pattern = re.compile(r'\b\d{1,2}月\d{1,2}日\b')
                year = time.strftime("%Y")
                date = year + '-' + date.replace('月', '-').replace('日', '')

                for link in linkNews.find_all('a', target="_blank"):
                    title = link.text
                    # 文章链接
                    href = link.get('href')
                    self.link_list.append([title, date, href])

    def get_update_link_list(self):
        # 获取语料的更新时间
        with open('update_config.json', 'r', encoding='utf-8') as f:
            update_config = json.load(f)
            website = self.type[0]
            categoty = self.type[1]
            update_time = update_config[website][categoty]
        newest_time = set()
        # 获取更新文章链接
        end_condition = 0  # 默认为已搜索完所有文章
        for url in self.page_list:
            if end_condition:
                # 已搜完最新文章
                break
            response = requests.get(url=url, headers=headers)
            response.encoding = 'UTF-8'
            html = BeautifulSoup(response.text, "html.parser")
            for linkNews in html.find_all('ul', class_="linkNews", style=False):
                # 文章发布时间
                date = linkNews.find('span').text
                date = date.strip('(').strip(')').strip()
                year = time.strftime("%Y")
                date = year + '-' + date.replace('月', '-').replace('日', '')
                newest_time.update([date])

                if date <= update_time:
                    # 文章已在库中，结束本次更新
                    end_condition = 1
                    break

                for link in linkNews.find_all('a', target="_blank"):
                    title = link.text
                    # 文章链接
                    href = link.get('href')
                    self.link_list.append([title, date, href])

        # 更新config最新时间
        with open('update_config.json', 'w', encoding='utf-8') as f:
            update_config[website][categoty] = list(newest_time)[-1]
            json.dump(update_config, f, ensure_ascii=False, indent=4)

    def get_text(self):
        # 获取文章内容并储存
        with open(self.path, 'w') as f:
            csv_writer = csv.writer(f, delimiter='\t')
            count = 0

            for link_li in self.link_list:
                title = link_li[0]
                date = link_li[1]
                url = link_li[2]
                response = requests.get(url=url, headers=headers)
                response.encoding = 'UTF-8'
                html = BeautifulSoup(response.text, "html.parser")

                # 文章关键字
                keywords = ''
                key = html.find('div', class_="keywords")
                if key is not None:
                    for word in key.find_all('a'):
                        keywords = keywords + ',' + word.text
                keywords = keywords.strip(',')

                passage = ''
                article = html.find('div', class_="article", id='article')
                if article is None:
                    continue
                for paragraph in article.find_all('p'):
                    passage += paragraph.text

                count += 1
                if count % 50 == 0:
                    print('抓取新浪网第{}篇...'.format(count))
                csv_writer.writerow([title, date, url, keywords, passage])

    def to_baidu(self, file_path):
        # 转为百度可用的格式
        with open(self.path, 'r', encoding='utf-8') as f:
            f_w = open(file_path, 'w', encoding='utf-8')
            reader = csv.reader(f, delimiter='\t')
            for line in reader:
                line = line[4]
                line = line.replace('\s+', '').replace('\n', '').replace('\t', '')
                for sent in line.split('。'):
                    sent = sent + '。'
                    dic = {}
                    dic['text'] = sent.strip()
                    dic['spo_list'] = ''
                    json.dump(dic, f_w, ensure_ascii=False)
                    f_w.write('\n')
            f_w.close()


class china_crawler(object):
    """
    爬取中华网武器数据（冷战后至今时间段）
    """

    def __init__(self, path):
        # 储存页面url
        self.page_list = []
        # 储存文章url
        self.link_list = []
        self.path = path

    def get_page_list(self):
        aircraft_url = 'https://weapon-p.china.com/?callback=jQuery1111006555436104261303_1597139654827&born_time=%E5%86%B7%E6%88%98%E5%90%8E%E8%87%B3%E4%BB%8A&weapon_type=%E9%A3%9E%E8%A1%8C%E5%99%A8&page={}'
        aircraft_page = 14
        ship_url = 'https://weapon-p.china.com/?callback=jQuery1111006555436104261303_1597139654827&born_time=%E5%86%B7%E6%88%98%E5%90%8E%E8%87%B3%E4%BB%8A&weapon_type=%E8%88%B0%E8%88%B9%E8%88%B0%E8%89%87&page={}'
        ship_page = 15
        gun_url = 'https://weapon-p.china.com/?callback=jQuery1111006555436104261303_1597139654827&born_time=%E5%86%B7%E6%88%98%E5%90%8E%E8%87%B3%E4%BB%8A&weapon_type=%E6%9E%AA%E6%A2%B0%E4%B8%8E%E5%8D%95%E5%85%B5&page={}'
        gun_page = 14
        tank_url = 'https://weapon-p.china.com/?callback=jQuery1111006555436104261303_1597139654827&born_time=%E5%86%B7%E6%88%98%E5%90%8E%E8%87%B3%E4%BB%8A&weapon_type=%E5%9D%A6%E5%85%8B%E8%A3%85%E7%94%B2%E8%BD%A6%E8%BE%86&page={}'
        tank_page = 4
        cannon_url = 'https://weapon-p.china.com/?callback=jQuery1111006555436104261303_1597139654827&born_time=%E5%86%B7%E6%88%98%E5%90%8E%E8%87%B3%E4%BB%8A&weapon_type=%E7%81%AB%E7%82%AE&page={}'
        cannon_page = 3
        missile_url = 'https://weapon-p.china.com/?callback=jQuery1111006555436104261303_1597139654827&born_time=%E5%86%B7%E6%88%98%E5%90%8E%E8%87%B3%E4%BB%8A&weapon_type=%E5%AF%BC%E5%BC%B9%E6%AD%A6%E5%99%A8&page={}'
        missile_page = 5
        space_url = 'https://weapon-p.china.com/?callback=jQuery1111006555436104261303_1597139654827&born_time=%E5%86%B7%E6%88%98%E5%90%8E%E8%87%B3%E4%BB%8A&weapon_type=%E5%A4%AA%E7%A9%BA%E8%A3%85%E5%A4%87&page={}'
        space_page = 14
        url_list = [aircraft_url, ship_url, gun_url, tank_url, cannon_url, missile_url, space_url]
        page_list = [aircraft_page, ship_page, gun_page, tank_page, cannon_page, missile_page, space_page]
        for i in range(len(url_list)):
            for page_no in range(1, page_list[i] + 1):
                self.page_list.append(url_list[i].format(page_no))

    def parse(self, url):
        # 查找文章链接
        response = requests.get(url=url, headers=headers)
        response.encoding = 'UTF-8'
        # html = BeautifulSoup(response.text, "html.parser")
        # links = html.find_all('a', {"href": re.compile('^(http://military.china.com/weapon/).+?(.html)$')})
        # page_links = set([link['href'] for link in links])
        json_string = response.text[response.text.find('{'):-1]
        json_data = json.loads(json_string)
        for weapon in json_data['rows']:
            self.link_list.append(weapon['redirect_url'])
            # sentce = weapon['abstracts']

    def get_link_list(self):
        for url in self.page_list:
            self.parse(url)

    def store_text(self):
        count = 0
        fp = open(self.path, 'w', encoding='utf-8')
        for url in self.link_list:
            response = requests.get(url=url, headers=headers)
            response.encoding = 'UTF-8'
            html = BeautifulSoup(response.text, "html.parser")
            # urls = html.find('div', {"class": 'basic-info cmn-clearfix'})
            source = html.find_all(class_='article-parameter-table')

            dic = {}
            weapon = html.h1
            if weapon:
                title = weapon.text
                dic[title] = {}
                for table in source:
                    for item in table.find_all('td'):
                        key = item.find('em').text.strip()
                        value = item.find('p').text.strip()
                        dic[title][key] = value
                if len(dic[title]) > 0:
                    count += 1
                    if count % 50 == 0:
                        print('抓取中华网第{}篇...'.format(count))
                    json.dump(dic, fp, ensure_ascii=False, indent=None)
                    fp.write('\n')
        fp.close()

    def to_KG(self, file_path):
        # 转为SPO格式
        with open(self.path, 'r', encoding='utf-8') as f:
            f_w = open(file_path, 'w', encoding='utf-8')
            for line in f.readlines():
                dic = json.loads(line)
                entity = list(dic.keys())[0]
                dic = list(dic.values())[0]
                # 选取前6个关系，不包含‘名称’
                i = 1
                for key, value in dic.items():
                    if key == '名称':
                        continue
                    if i > 6:
                        break
                    new_dic = {}
                    spo = {}
                    spo['subject_type'] = ''
                    spo['subject'] = entity
                    spo['predicate'] = key
                    spo['object_type'] = ''
                    spo['object'] = value
                    new_dic['spo_list'] = spo
                    new_dic['sent'] = ''
                    new_dic['url'] = ''
                    new_dic['date'] = ''

                    json.dump(new_dic, f_w, ensure_ascii=False)
                    f_w.write('\n')
                    i += 1
