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
    mentor_file = open('./mentors.json', 'r', encoding='utf-8')
    mentor_infos = json.loads(mentor_file.read())
    if os.path.exists('./avatar') == False:
        os.mkdir('./avatar')
    url = 'http://www.it.fudan.edu.cn/Data/List/azc'
    req = requests.get(url, timeout=10)
    print(req.apparent_encoding)
    soup = BeautifulSoup(req.text, 'html.parser', from_encoding='utf-8')
    mentors = soup.find_all('a', 'people')

    pattern = re.compile(r'^/Data/View/')

    gg_mentors = []

    fields = ['研究兴趣', '学术任职', '获奖情况', '学习工作经历', '授课情况', '论文专著']
    for mentor in mentors:
        mentor_url = mentor.get('href')
        if pattern.match(mentor_url) == None:
            continue
        name = mentor.contents[0].strip()
        mentor_info = None
        mentor_index = None
        for index, mentor_exist in enumerate(mentor_infos):
            if mentor_exist.get('姓名') == name:
                mentor_info = mentor_exist
                mentor_index = index
                break
        try:
            mentor_req = requests.get('http://www.it.fudan.edu.cn'+mentor_url, timeout=10)
            mentor_soup = BeautifulSoup(mentor_req.text, 'html.parser', from_encoding='utf-8')
            for i in range(6):
                tab = mentor_soup.find_all('div', class_='tabcss', id='tab_{}'.format(i+1))[0]
                mentor_info[fields[i]] = tab.get_text().split('\n')
                while '' in mentor_info[fields[i]]:
                    mentor_info[fields[i]].remove('')
                print(fields[i], ':', mentor_info[fields[i]])

            mentor_infos[mentor_index] = mentor_info
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
