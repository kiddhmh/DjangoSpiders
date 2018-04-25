from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from CCICApp.models import vvebo, wechat, zhihu

def index(request):
    return render_to_response('index.html')


def index_search(request):
    # 获取用户提交信息,关键字为空提示用户
    selectWeb = ''
    keyword = ''
    if 'selectWeb' in request.GET:
        selectWeb = request.GET['selectWeb']
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']

    print('选择的网页是', selectWeb)
    print('搜索的关键词是', keyword)
    context = {}
    resultNumbers = 0

    # 判断是哪个网址哪个关键词,数据库是否存在,不存在提示爬取
    if selectWeb == 'weibo':
        resultNumbers = vvebo.objects.filter(keyword=keyword).count()
    elif selectWeb == 'zhihu':
        resultNumbers = zhihu.objects.filter(keyword=keyword).count()
    elif selectWeb == 'wechat':
        resultNumbers = wechat.objects.filter(keyword=keyword).count()
    else:
        print('不可能触发的', selectWeb)

    context['resultNumbers'] = resultNumbers
    context['selectWeb'] = selectWeb
    context['keyword'] = keyword

    return render(request, 'searchResult.html', context)


'''
def index_search(request):
    print('点击了提交表单', request.GET)

    response = ''
    response1 = ''

    list = vvebo.objects.all()

    for var in list:
        html = "<li>" + var.device + "</li>"
        response1 += html
    response = response1
    return HttpResponse(
        "<p>查询后结果为</p><ul>"
            + response +
        "</ul>"
    )
'''