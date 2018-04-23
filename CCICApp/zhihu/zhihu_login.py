import requests
import time, json, os, sys, subprocess, queue
from bs4 import BeautifulSoup as BS, BeautifulSoup


class ZhiHuLogin(object):
    TYPE_PHONE_NUM = 'phone_num'
    TYPE_EMAIL = 'email'
    loginURL = r'http://www.zhihu.com/login/{0}'
    homeURL = r'http://www.zhihu.com'
    captchaURL = r"http://www.zhihu.com/captcha.gif"
    user_agent_list = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0)Gecko/20100101 Firefox/55.0'
                  ,'Mozilla/5.0 (Windows NT 6.1; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90Safari/537.36'
                  ,'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0;rv:11.0) like Gecko'
                  ,'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0)Gecko/20100101 Firefox/54.0'
                  ,'Mozilla/5.0 (Windows NT 6.1; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113Safari/537.36'
                  ,'Mozilla/5.0 (Windows NT 10.0; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104Safari/537.36']
    headers = {
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    captchaFile = os.path.join(sys.path[0], "captcha.gif")
    cookieFile = os.path.join(sys.path[0], "cookie")

    def __init__(self, searchDic):
        self.__user_auth = queue.Queue()
        self.__user_agent = queue.Queue()
        self.__islogin = False
        os.chdir(sys.path[0])
        self.__session = requests.Session()
        authorization_path = os.path.join(sys.path[0], 'authorization')

        if os.path.exists(authorization_path) and os.path.isfile(authorization_path):
            with open(os.path.join(authorization_path), 'r') as f:
                while True:
                    auth = f.readline()
                    if not auth or auth == '':
                        break
                    else:
                        self.__user_auth.put(str(auth))
        else:
            print("Error:因登录系统无法获取身份认证信息authorization，"
                  "请自行获取并在同级目录下新建名为authorization文件并将authorization写入，"
                  "换行分隔多个。")

        for user_agent in self.user_agent_list:
            self.__user_agent.put(user_agent)
            self.__user_agent.put(user_agent)

        self.__session.headers = self.headers
        self.__cookie = self.loadCookie()
        if self.__cookie:
            self.__session.cookies.update(self.__cookie)
        else:
            self.__username = searchDic['username']
            self.__password = searchDic['password']
            self.__login()

    def __login(self):
        self.__islogin = True
        self.__loginURL = self.loginURL.format(self.__getUsernameType())
        print("self.__loginURL = " + self.__loginURL)
        html = self.open(self.homeURL).text
        soup = BeautifulSoup(html, "html.parser")
        _xsrf = soup.find("input", {"name": "_xsrf"})
        if _xsrf == None:
            print("_xsrf = None")
        else:
            print("_xsrf = " + _xsrf)

        while True:
            captcha = self.open(self.captchaURL).content
            with open(self.captchaFile, 'wb') as output:
                output.write(captcha)
            print("已打开验证码图片，请识别:")
            # subprocess.call(self.captchaFile, shell=True)
            print("子进程开启")
            captcha = input("请输入验证码:")
            os.remove(self.captchaFile)
            # 登录表单
            data = {
                "_xsrf": _xsrf,
                "password": self.__password,
                "remember_me": "true",
                self.__getUsernameType(): self.__username,
                "captcha": captcha
            }
            print(data)
            # 提交登录表单
            res = self.__session.post(self.__loginURL, data=data)
            if res.status_code == 200:
                print("登录成功")
                self.__saveCookie()
                break
            else:
                print("登录失败,错误信息:", res.json()["msg"])

    def __getUsernameType(self):
        """判断用户名类型
        经测试，网页的判断规则是纯数字为phone_num，其他为email
        """
        if self.__username.isdigit():
            return self.TYPE_PHONE_NUM
        return self.TYPE_EMAIL

    def __saveCookie(self):
        with open(self.cookieFile, "w") as output:
            sessions = self.__session.cookies
            cookies = sessions.get_dict()
            json.dump(cookies, output)
    def loadCookie(self):
        if os.path.exists(self.cookieFile):
            with open(self.cookieFile, "r") as f:
                cookie = json.load(f)
                print(cookie)
                return cookie
        return None

    def open(self, url, auth=False, delay=10, timeout=20):
        # if delay:
        #     time.sleep(delay)

        user_agent = self.__user_agent.get()
        self.headers['User-Agent'] = ''+user_agent+''
        self.__user_agent.put(user_agent)

        if auth:
            user_auth = self.__user_auth.get()
            self.headers['authorization'] = user_auth.replace("\n", '')
            self.__user_auth.put(user_auth)
        self.__session.headers = self.headers
        return self.__session.get(url, timeout=timeout)
    def getSession(self):
        return self.__session

