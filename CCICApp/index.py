from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from CCICApp.models import vvebo

def index(request):
    return render_to_response('index.html')


def index_search(request):
    print('点击了提交表单', request.GET)

    list = vvebo.objects.all()
    context = {}
    context['resultNumbers'] = list.count()

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