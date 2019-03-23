from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers

import json

from .models import User

@require_http_methods(["POST"])
def login(request):
    req_json = json.loads(request.read(), encoding='utf-8')
    print(req_json)
    User.objects.create(openid=req_json['openid'], session_key=req_json['session_key'], name='90')
    userSet = User.objects.filter(openid=req_json['openid'])
    user = userSet[0]
    user.openid = '345'
    user.save()
    print(user.openid)
    user_json = serializers.serialize('json', [user, ])
    return HttpResponse(user_json, content_type="application/json")