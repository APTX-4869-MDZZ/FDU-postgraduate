#!usr/bin/env python3
# -*- coding:utf-8 -*-
import urllib.request
import requests
import json
import re
import os
from bs4 import BeautifulSoup
from pypinyin import lazy_pinyin

def main():
    if os.path.exists('./avatar') == False:
        os.mkdir('./avatar')
    url = 'http://www.it.fudan.edu.cn/Data/List/azc'
    req = requests.get(url, timeout=10)
    print(req.apparent_encoding)
    soup = BeautifulSoup(req.text, 'html.parser', from_encoding='utf-8')
    mentors = soup.find_all('a', 'people')

    mentor_infos = []
    pattern = re.compile(r'^/Data/View/')

    gg_mentors = []

    for mentor in mentors:
        mentor_url = mentor.get('href')
        if pattern.match(mentor_url) == None:
            continue
        name = mentor.contents[0].strip()
        mentor_info = {
            '姓名': name
        }
        try:
            mentor_req = requests.get('http://www.it.fudan.edu.cn'+mentor_url, timeout=10)
            mentor_soup = BeautifulSoup(mentor_req.text, 'html.parser', from_encoding='utf-8')
            intro = mentor_soup.find_all('div', class_='teach-intro')[0].contents
            for each in intro:
                if isinstance(each, str):
                    continue
                if each.get('class', [0])[0] == 'title':
                    mentor_info['系'] = each.img.text
                else:
                    contents = each.contents[1].split('：')
                    if '，' in contents[1]:
                        mentor_info[contents[0]] = [x.strip()
                                                    for x in contents[1].split('，')]
                    elif '、' in contents[1]:
                        mentor_info[contents[0]] = [x.strip()
                                                    for x in contents[1].split('、')]
                    else:
                        mentor_info[contents[0]] = contents[1].strip()
            src = mentor_soup.find('div', 'teach-right').img.get('src')
            if src != None and src != '':
                img_name = '_'.join(lazy_pinyin(mentor_info['姓名']))
                urllib.request.urlretrieve(
                    'http://www.it.fudan.edu.cn'+src, './avatar/{}.jpg'.format(img_name))
            mentor_infos.append(mentor_info)
            print(name, 'ok')
        except Exception as e:
            gg_mentors.append(name)
            continue

    with open('./gg_mentors.json', 'w', encoding='utf-8') as file:
        json.dump(gg_mentors, file, ensure_ascii=False)

    with open('./mentors.json', 'w', encoding='utf-8') as file:
        json.dump(mentor_infos, file, ensure_ascii=False)
        print('Done.')


if __name__ == '__main__':
    main()
