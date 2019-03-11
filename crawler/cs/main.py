#!usr/bin/env python3
# -*- coding:utf-8 -*-
import urllib
import json
import re
import os
from bs4 import BeautifulSoup
from pypinyin import lazy_pinyin


def main():
    if os.path.exists('./avatar') == False:
        os.mkdir('./avatar')
    url = 'http://www.cs.fudan.edu.cn/?cat=132&t1=zz3'
    req = urllib.request.urlopen(url, timeout=10)
    soup = BeautifulSoup(req.read(), 'lxml')
    cs_mentors = soup.find('dl', class_='ui-tch-dl').find_all('a')

    mentor_infos = []
    pattern = re.compile(r'^http://w+')

    gg_mentors = []

    for cs_mentor in cs_mentors:
        mentor_url = cs_mentor.get('href')
        if pattern.match(mentor_url) == None:
            continue
        name = cs_mentor.contents[0]
        mentor_info = {
            '姓名': name
        }
        try:
            mentor_req = urllib.request.urlopen(mentor_url, timeout=10)
            mentor_soup = BeautifulSoup(mentor_req.read(), 'lxml')
            intro = mentor_soup.find_all('div', class_='t-inf ui-btmline')
            for each in intro:
                contents = each.contents[0].split('：')
                if '，' in contents[1]:
                    mentor_info[contents[0]] = [x.strip()
                                                for x in contents[1].split('，')]
                elif '、' in contents[1]:
                    mentor_info[contents[0]] = [x.strip()
                                                for x in contents[1].split('、')]
                else:
                    mentor_info[contents[0]] = contents[1].strip()
            style = mentor_soup.find('div', class_='pic-1').get('style')
            if style != None and style != '':
                avatar = re.findall(r'[a-zA-z]+://[^\s]*.jpg', style)
                img_name = '_'.join(lazy_pinyin(name))
                urllib.request.urlretrieve(
                    avatar[0], './avatar/{}.jpg'.format(img_name))
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
