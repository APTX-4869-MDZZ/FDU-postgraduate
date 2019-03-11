#!usr/bin/env python3
# -*- coding:utf-8 -*-
import requests
import json
import re
import os
from pypinyin import lazy_pinyin


def main():
    if os.path.exists('./avatar') == False:
        os.mkdir('./avatar')
    url = 'http://www.software.fudan.edu.cn/drupal/software/api/teachers?group=teacher'
    headers = {'Accept-Encoding': 'deflate','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}
    res = requests.get(url,headers=headers).json()
    res_str = json.dumps(res)
    result = json.loads(res_str)
    imgs = []
    mentors = []
    for r in result:
        img = {}
        img['name'] = r['field_name']
        img['imgUrl'] = r['field_avatar']
        imgs.append(img)
        mentorInfo = {}
        mentorInfo['姓名'] = r['field_name'].strip()
        position = r['field_position']
        reObj = re.compile('[,，、]')
        positions = ''
        if reObj.search(position):
            positions = [x.strip()
                        for x in re.split('[,，、]',position)]
        else:
            positions = position.strip()
        mentorInfo['职称'] = positions
        mentorInfo['电话'] = r['field_phone'].strip()
        mentorInfo['邮件'] = r['field_email'].strip()
        mentorInfo['地址'] = r['field_officer'].strip()
        mentorInfo['学位'] = ''
        fields = ''
        field = r['field_major']
        if reObj.search(field):
            fields = [x.strip()
                        for x in re.split('[,，、]',field)]
        else:
            fields = field.strip()
        mentorInfo['研究领域'] = fields
        mentors.append(mentorInfo)
    for img in imgs:
        response = requests.get(img['imgUrl'])
        if response.status_code == 200:
            img_name = '_'.join(lazy_pinyin(img['name']))
            open('./avatar/{}.jpg'.format(img_name),'wb').write(response.content)

    with open('./mentors.json', 'w', encoding='utf-8') as file:
        json.dump(mentors, file, ensure_ascii=False)
        print('Done.')











if __name__ == '__main__':
    main()
