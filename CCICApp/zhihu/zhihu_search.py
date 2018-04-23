from CCICApp.zhihu.zhihu_login import ZhiHuLogin

class ZhiHuSearch(object):
    homeURL = 'https://www.zhihu.com'
    def __init__(self, searchDic):
        self.__search_text = searchDic['keyword']
        self.__loginclient = ZhiHuLogin(searchDic)  # 初始化，若没登录则登录

    # addq = add + q 添加参数的意思
    def do_search(self, url: object, addq: object, auth: object = False) -> object:
        self.__searchURL = url
        if addq:
            # 拼接搜索url
            self.__searchURL = self.homeURL + self.__searchURL + self.__search_text
        soup = self.__loginclient.open(self.__searchURL, auth=auth)
        return soup
