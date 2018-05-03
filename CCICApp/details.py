from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from CCICApp.models import vvebo, wechat, zhihu
from django.core import serializers
import json


def detail(request):
    return render_to_response('details.html')



def ajxdetail(request):
    print('发送ajax')

    keywordID = int(request.GET.get('id'))
    selectWeb = str(request.GET.get('selectWeb'))

    print('详情页ID:', keywordID)
    print('详情页网址:', selectWeb)

        # 查询
    if selectWeb == "weibo":
        result =  serializers.serialize("json", vvebo.objects.order_by('id')[keywordID - 1:keywordID])

    if selectWeb == "zhihu":
        result =  serializers.serialize("json", zhihu.objects.order_by('id')[keywordID - 1:keywordID])

    if selectWeb == "wechat":
        result =  serializers.serialize("json", wechat.objects.order_by('id')[keywordID - 1:keywordID])

    return_json = {
        'statusCode': 1,
        'result': result
    }

    print('详情页内容是', result)

    return HttpResponse(json.dumps(return_json), content_type='application/json')