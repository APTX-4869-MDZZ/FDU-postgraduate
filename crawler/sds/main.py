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
    src_end_pattern = re.compile(r'.*.png$')
    if os.path.exists('./avatar') == False:
        os.mkdir('./avatar')
    urls = ['http://www.sds.fudan.edu.cn/wp/?p=1009', 'http://www.sds.fudan.edu.cn/wp/?p=211', 'http://www.sds.fudan.edu.cn/wp/?p=1097']
    mentor_infos = []
    for url in urls:
        req = requests.get(url, timeout=10)
        soup = BeautifulSoup(req.text, 'html.parser', from_encoding='utf-8')
        mentors = soup.find_all('tr')
        for mentor in mentors:
            name = mentor.find_all('h4')[0].text
            mentor_info = {
                '姓名': name
            }
            intro = mentor.find_all('p')[0].text
            intro_sentence = intro.split('。')
            for i, sentence in enumerate(intro_sentence):
                sub_sentences = sentence.split('，')
                for j, sub_sentence in enumerate(sub_sentences):
                    if sub_sentence.find('学位') != -1:
                        mentor_info['学习工作情况'] = [sub_sentence]
                        mentor_info['职称职位'] = []
                        mentor_info['职称职位'].extend(intro_sentence[0: i])
                        mentor_info['职称职位'].extend(sub_sentences[0: j])
                    if sub_sentence.find('工作') != -1 or sub_sentence.find('博士后') != -1:
                        if mentor_info.get('学习工作情况'):
                            mentor_info['学习工作情况'].append(sub_sentence)
                        else:
                            mentor_info['学习工作情况'] = [sub_sentence]

            for i, sentence in enumerate(intro_sentence):
                if mentor_info.get('研究方向', '') == '' and sentence.find('研究') != -1 and sentence.find('研究员') == -1 and sentence.find('大学') == -1:
                    sub_sentences = sentence.split('，')
                    mentor_info['研究方向'] = []
                    for j, sub_sentence in enumerate(sub_sentences):
                        if sub_sentence.find('发表') != -1 or sub_sentence.find('会议') != -1 or sub_sentence.find('期刊') != -1 or sub_sentence.find('论文') != -1:
                            mentor_info['论文专著获奖'] = sub_sentences[j:]
                            mentor_info['论文专著获奖'].extend(intro_sentence[i+1:])
                            break
                        else:
                            mentor_info['研究方向'].append(sub_sentence)
                    if mentor_info.get('职称职位', '') == '':
                        mentor_info['职称职位'] = intro_sentence[0: i]
                elif mentor_info.get('研究方向'):
                    if mentor_info.get('论文专著获奖'):
                        mentor_info['论文专著获奖'].extend(intro_sentence[i:])
                    else:
                        mentor_info['论文专著获奖'] = intro_sentence[i:]
                    break
            while '' in mentor_info['论文专著获奖']:
                mentor_info['论文专著获奖'].remove('')

            src = mentor.find('img', ('aligncenter', 'wp-image-1014')).get('src')
            if src != None and src != '':
                img_name = '_'.join(lazy_pinyin(mentor_info['姓名']))
                if src_end_pattern.match(src):
                    urllib.request.urlretrieve(src, './avatar/{}.png'.format(img_name))
                else:
                    urllib.request.urlretrieve(src, './avatar/{}.jpg'.format(img_name))
            mentor_infos.append(mentor_info)
            print(name, 'ok')

    with open('./mentors.json', 'w', encoding='utf-8') as file:
        json.dump(mentor_infos, file, ensure_ascii=False)
        print('Done.')


if __name__ == '__main__':
    main()
