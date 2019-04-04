from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
import requests

import json

from .models import User

@require_http_methods(["POST"])
def login(request):
    req_json = json.loads(request.read(), encoding='utf-8')
    js_code = req_json['code']
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=wxb42e944a8a905558&secret=0ab9ad927dd1caf7cc76779ab67891dc&js_code={}&grant_type=authorization_code'.format(js_code)
    wxresponse = requests.get(url)
    wxresponse_json = json.loads(wxresponse.text)
    print(wxresponse_json)
    res = {
        'success': True
    }
    if 'errcode' in wxresponse_json:
        User.objects.create(openid=wxresponse_json['openid'], session_key=wxresponse_json['session_key'], unionid=wxresponse_json['unionid'])
        res['user']=wxresponse_json['session_key']
    else:
        print(wxresponse_json['errcode'], wxresponse_json['errmsg'])
        res['success'] = False
    return HttpResponse(json.dumps(res), content_type="application/json")
