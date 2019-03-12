#!usr/bin/env python3
# -*- coding:utf-8 -*-
import urllib
import json
import os
import re
from bs4 import BeautifulSoup
from pypinyin import lazy_pinyin


def main():
    if os.path.exists('./avatar') == False:
        os.mkdir('./avatar')
    url = 'https://sme.fudan.edu.cn/info/list?channelcode=anzhicheng'
    req = urllib.request.urlopen(url, timeout=10)
    soup = BeautifulSoup(req.read(), 'lxml')
    mentors = soup.find('div', class_='teacher-list').find_all('a')

    mentor_infos = []
    gg_mentors = []

    for mentor in mentors:
        href = mentor.get('href')
        if re.match(r'^/', href) == None:
            continue
        name = mentor.contents[0]
        try:
            mentor_url = 'https://sme.fudan.edu.cn{}'.format(href)
            mentor_req = urllib.request.urlopen(mentor_url, timeout=10)
            mentor_soup = BeautifulSoup(mentor_req.read(), 'lxml')
            # get mentor info
            intro = mentor_soup.find('div', class_='teacher-info')
            # 头像
            avatar_src = intro.find('img').get('src')
            avatar_url = 'https://sme.fudan.edu.cn{}'.format(avatar_src)
            avatar_name = '_'.join(lazy_pinyin(name))
            urllib.request.urlretrieve(
                avatar_url, './avatar/{}.jpg'.format(avatar_name))
            # 职称
            prof_tag = intro.find_all('span', class_='xhu')
            prof_tag = [pt.contents[0] for pt in prof_tag]

            mentor_info = {
                '姓名': name,
                '职称': prof_tag
            }
            # 电话 邮箱 地址 研究所
            others = intro.find_all('p', class_='teacher-info-line')
            for o in others:
                key = o.find('span', class_='label').contents[0].strip()
                value = o.find('span', class_='kij').contents[1].strip()
                mentor_info[key] = value
            # 研究方向 ...
            # others1 = intro.find('div', class_='teacher-right').find_all('p')
            # others1 = [o.contents for o in others1]

            # i = 0
            # cur_key = None
            # while i < len(others1):
            #     tag_name = others1[i][0].name
            #     if tag_name == 'strong':
            #         cur_key = others1[i][0].contents[0]
            #         mentor_info[cur_key] = []
            #         i = i + 1
            #     elif tag_name == 'span':
            #         mentor_info[cur_key].append(others1[i][1])
            #         i = i + 1
            #     elif tag_name == 'br':
            #         cur_key = None
            #         i = i + 1
            #         continue
            #     else:
            #         i = i + 1
            #         continue
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


if __name__ == "__main__":
    main()
