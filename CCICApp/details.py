from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from CCICApp.models import vvebo, wechat, zhihu


def detail(request):
    print('进入了详情页')

    if 'selectWeb' in request.GET:
        selectWeb = request.GET['selectWeb']
        print('详情页网址:', selectWeb)
    if 'id' in request.GET:
        keywordID = request.GET['id']
        print('详情页ID:', keywordID)

    # 查询


    return render_to_response('details.html')