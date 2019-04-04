from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
import requests

import json
import hashlib

from .models import User
from tools import constant

@require_http_methods(["POST"])
def login(request):
    req_json = json.loads(request.read(), encoding='utf-8')
    js_code = req_json['code']
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'.format(constant.appid, constant.secret_key, js_code)
    print(js_code)
    wxresponse = requests.get(url)
    wxresponse_json = json.loads(wxresponse.text)
    print(wxresponse_json)
    res = {
        'success': True
    }
    if 'errcode' not in wxresponse_json:
        m = hashlib.md5()
        session_seed = wxresponse_json['openid']+wxresponse_json['session_key']
        session_seed = session_seed.encode('utf-8')
        m.update(session_seed)
        sessionid = m.hexdigest()
        User.objects.create(openid=wxresponse_json['openid'], session_key=wxresponse_json['session_key'], sessionid=sessionid)
        request.session['id'] = sessionid
    else:
        print(wxresponse_json['errcode'], wxresponse_json['errmsg'])
        res['success'] = False
    return HttpResponse(json.dumps(res), content_type="application/json")

@require_http_methods(["GET"])
def test(request):
    sessionid = request.session.get('id', False)
    if not sessionid:
        return HttpResponse('get no session', content_type="application/json")
    else:
        user = User.objects.get(sessionid=sessionid)
        print(user.openid)
        return HttpResponse('find it', content_type="application/json")
