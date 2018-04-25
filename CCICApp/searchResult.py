from django.http import HttpResponse
from django.shortcuts import render_to_response
from CCICApp.models import vvebo
from django.core import serializers
import json

def searchResult(request):
    page = int(request.GET.get('page'))
    first = (page - 1) * 10
    end = page * 10
    resultList =  serializers.serialize("json", vvebo.objects.order_by('id')[first:end])
    print('请求的是第几页', page)
    print('返回结果是', resultList)

    return_json = {
        'statusCode': 1,
        'result': resultList
    }

    return HttpResponse(json.dumps(return_json), content_type='application/json')