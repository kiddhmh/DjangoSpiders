from django.http import HttpResponse
from django.shortcuts import render_to_response
from CCICApp.zhihu.zhihu_deal import ZhiHuDeal


def search_zhihu(request):
    return render_to_response('zhihu.html')

def searchzhihu(request):
    searchDic = {}
    request.encoding = 'utf-8'
    if 'username' in request.GET:
        searchDic['username'] = request.GET['username']
    if 'password' in request.GET:
        searchDic['password'] = request.GET['password']
    if 'keyword' in request.GET:
        searchDic['keyword'] = request.GET['keyword']
    print('准备开始调用:', searchDic)
    run(searchDic)
    print('结束调用')
    return HttpResponse('正在查询,请稍后...')

def run(searchDic):
    try:
        ZhiHuDeal(searchDic)
    except Exception as e:
        print(e.with_traceback())
    finally:
        print("程序执行结束。")
