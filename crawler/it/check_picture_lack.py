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
    req = requests.get(url)
    print(req.apparent_encoding)
    soup = BeautifulSoup(req.text, 'html.parser', from_encoding='utf-8')
    mentors = soup.find_all('a', 'people')

    mentor_infos = []
    pattern = re.compile(r'^/Data/View/')
    src_pattern = re.compile(r'^http')
    src_end_pattern = re.compile(r'.*.png$')

    for mentor in mentors:
        mentor_url = mentor.get('href')
        if pattern.match(mentor_url) == None:
            continue
        name = mentor.contents[0].strip()
        # try:
        mentor_req = requests.get('http://www.it.fudan.edu.cn'+mentor_url)
        mentor_soup = BeautifulSoup(mentor_req.text, 'html.parser', from_encoding='utf-8')
        intro = mentor_soup.find_all('div', class_='teach-intro')[0].contents
        for each in intro:
            if isinstance(each, str):
                continue
        src = mentor_soup.find('div', 'teach-right').img.get('src')
        if src != None and src != '':
            img_name = '_'.join(lazy_pinyin(name))
            if src_pattern.match(src):
                if src_end_pattern.match(src):
                    urllib.request.urlretrieve(src, './avatar/{}.png'.format(img_name))
                    if os.path.exists('./avatar/{}.jpg'.format(img_name)):
                        os.remove('./avatar/{}.jpg'.format(img_name))
            else:
                if src_end_pattern.match(src):
                    if os.path.exists('./avatar/{}.jpg'.format(img_name)):
                        os.remove('./avatar/{}.jpg'.format(img_name))
                    urllib.request.urlretrieve('http://www.it.fudan.edu.cn'+src, './avatar/{}.png'.format(img_name))
        print(name, 'ok')
        # except Exception as e:
        #     gg_mentors.append(name)
        #     continue

if __name__ == '__main__':
    main()
