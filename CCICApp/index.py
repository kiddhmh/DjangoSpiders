from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    return render_to_response('index.html')


def index_search(request):
    print('点击了提交表单', request)


def indexx(request):
    return render_to_response('indexx.html')