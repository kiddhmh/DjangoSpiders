"""CCICSpiders URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.views.static import serve
from CCICApp.weibo import downloadData
from CCICApp.zhihu import run
from CCICApp import index

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index$', index.index),
    url(r'^weibo-search$', downloadData.search_weibo),
    url(r'^weibo$', downloadData.searchweibo),
    url(r'^zhihu-search$', run.search_zhihu),
    url(r'^zhihu$', run.searchzhihu),

    url(r'^medias/(?P<path>.*)$', serve, {'document_root': '../DjangoSpiders/templates/images'}),
]
