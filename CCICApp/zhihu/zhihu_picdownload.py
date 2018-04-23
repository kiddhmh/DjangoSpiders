import requests, os, sys, datetime, time, shutil
from urllib import request
class ZhiHuPicDownload(object):
    __path = os.path.join(sys.path[0], datetime.datetime.now().strftime('%Y-%m-%d'))
    def __init__(self, text, delay=2):
        self.__delay = delay
        self.__path = os.path.join(self.__path, text)
        if os.path.exists(self.__path) and os.path.isdir(self.__path):
            shutil.rmtree(self.__path)
            os.mkdir(self.__path)
        else:
            os.mkdir(self.__path)
    def doDownload(self, urlorlist):
        if isinstance(urlorlist, list):
            for url in urlorlist:
                self.__download(url)
        else:
            self.__download(urlorlist)
    def __download(self, url):
        try:
            if url is None:
                return
            if self.__delay:
                time.sleep(self.__delay)
            res = requests.get(url)
            if res.status_code == 200:
                print("下载成功，正在保存图片："+url)
                name = url.split('/')[-1]
                print(type(name))
                with open(os.path.join(self.__path, name), 'wb') as f:
                    f.write(res.content)
            else:
                print("下载失败:" + str(res.status_code) + " : " + str(res.reason)+':'+url)
                return
        except Exception as e:
            print("保存失败：" + e.args)
