import datetime, json, os, re, sys, time, pymysql
from bs4 import BeautifulSoup
from CCICApp.zhihu.zhihu_search import ZhiHuSearch
from CCICApp.zhihu.zhihu_picdownload import ZhiHuPicDownload


class ZhiHuDeal(object):
    #获取话题列表页面url
    __search_url = '/search?type=content&q='
    #获取更多话题列表url
    __search_more = "/r/search?correction=1&type=content&offset={0}&q="
    __search_offset = 0
    __search_limit = 10
    __answers_more_limit = 20
    def __init__(self, searchDic):

        # # 获取今日的工作文件夹，若没有则创建
        # self.__dirpath = os.path.join(sys.path[0], datetime.datetime.now().strftime('%Y-%m-%d'))
        # if not os.path.exists(self.__dirpath) or not os.path.isdir(self.__dirpath):
        #     os.mkdir(self.__dirpath)

        # 链接数据库
        db = pymysql.connect(host='localhost',user='root', password='yinling2965', port=3306)
        cursor = db.cursor()
        # 如果数据库不存在，新建数据库
        cursor.execute("CREATE DATABASE IF NOT EXISTS zhihu_spider DEFAULT CHARACTER SET utf8mb4_unicode_cWY")
        db.close()

        # self.__text:搜索关键词
        self.__text = searchDic['keyword']
        # ZhiHuSearch() 初始化时执行登录
        self.__search = ZhiHuSearch(searchDic)

        # 暂时屏蔽图片下载功能
        # self.__zhihuPic = ZhiHuPicDownload(self.__text, 5)

        # 新建此关键词的文件
        with open(os.path.join(self.__dirpath, self.__text + ".txt"), 'w') as f:
            f.truncate()

        # 如果该关键词数据库表不存在，新建数据库表，表名不允许中文，故转换为UTF-8并去掉开头结尾和\x
        db = pymysql.connect(host='localhost',user='root', password='yinling2965', port=3306, db='zhihu_spider', charset="utf8")
        cursor = db.cursor()
        self.__table_name = str(self.__text.encode(encoding='UTF-8' ,errors='strict'))[2:-1].replace("\\x", "")
        print(self.__table_name)
        sql = "CREATE TABLE IF NOT EXISTS " \
              + self.__table_name \
              + " (" \
              + "keyword VARCHAR(255) NOT NULL, " \
              + "question_id VARCHAR(255) NOT NULL, " \
              + "question_name VARCHAR(255) NOT NULL, " \
              + "answer_id VARCHAR(255) NOT NULL, " \
              + "content LONGTEXT NOT NULL, " \
              + "date VARCHAR(255) NOT NULL, " \
              + "voteup_count INT NOT NULL, " \
              + "author VARCHAR(255) NOT NULL, " \
              + "PRIMARY KEY (answer_id))"
        print(sql)
        cursor.execute(sql)
        db.close()
        self.__findAndDealSubject(self.__search_url)

    # 解析搜索页，从中提取问题列表，遍历直到没有新的问题为止
    def __findAndDealSubject(self, url):
        result = self.__search.do_search(url, True)
        if result.status_code == 200:
            if result.encoding == 'utf-8':
                html = result.text
            else:
                list = json.loads(result.content)['htmls']
                html = ""
                for i in range(len(list)):
                    html += list[i]
        else:
            print("服务器链接失败:"+str(result.status_code))
            return
        soup = BeautifulSoup(html, "html.parser")
        lilist = soup.find_all("li", attrs={'class': re.compile("item")})
        self.__deal_list_subject(lilist)
        self.__search_offset += self.__search_limit # 按步长更新偏移量
        if len(lilist) is not 0:
            search_more = self.__search_more.format(str(self.__search_offset))
            self.__findAndDealSubject(search_more) # 继续迭代直到lilist长度为零

    # 遍历搜索页中解析出来的list，剔除里面的专栏文章，剩下的是问题
    def __deal_list_subject(self, list):
        if len(list) == 0:
            return
        for i in range(len(list)):
            a = list[i].find("a", attrs={'class': re.compile("js-title-link")})
            if a is not None:
                href = a.get('href')
                print(href)
                if not 'https://zhuanlan.zhihu.com' in href: # 排除知乎专栏
                    self.__findAndDealAnswer(href)
                else:
                    continue

    def __findAndDealAnswer(self, url):
        result = self.__search.do_search(self.__search.homeURL + url, False)
        if result.status_code == 200:
            html = result.content.decode('utf-8')

            soup = BeautifulSoup(html, "html.parser")

            # self.__findAndDown(html, {'class': re.compile("origin_image zh-lightbox-thumb lazy")})
            question_id = soup.find('meta', attrs={'itemprop': 'url'}).get("content").replace(self.__search.homeURL+"/question/","")

            data_state = soup.find('div', attrs={'id': 'data'}).get("data-state")
            datas = json.loads(data_state)
            url = datas['question']['answers'][question_id]['next'].replace(self.__search.homeURL, "")

            meta = soup.find('meta', attrs={'itemprop': re.compile("name")})
            question_name = meta.get("content")
            self.__write("\n\n\n\n======================================================="+question_name+"=============================================\n", None)
            answers = datas['entities']['answers']
            for answer_id in answers:
                content = BeautifulSoup(answers[answer_id]['content'], "html.parser").get_text()
                date = datetime.datetime.fromtimestamp(answers[answer_id]['updatedTime']).strftime('%Y-%m-%d')
                voteup_count = int(answers[answer_id]['voteupCount'])
                author = answers[answer_id]['author']['name']
                self.__write(content + "\n", author)
                # 将此条答案写入数据库
                self.__saveToMySQL(question_id, question_name, answer_id, content, date, voteup_count, author)

            self.__continueLoadAnswers(url, question_id, question_name)
        else:
            print("服务器链接失败:" + str(result.status_code) + " : " + str(result.reason))
            return

    def __continueLoadAnswers(self, url, question_id, question_name):
        url_more = url.replace('limit=5', 'limit=' + str(self.__answers_more_limit))
        result = self.__search.do_search(url_more, False, auth=True)
        if result.status_code == 200:
            response = json.loads(result.content.decode('utf-8'))
            paging = response['paging']
            datas = response['data']
            for data in datas:
                # self.__findAndDown(data['content'], {})
                answer_id = data['id']
                content = BeautifulSoup(data['content'], "html.parser").get_text()
                date = datetime.datetime.fromtimestamp(data['updated_time']).strftime('%Y-%m-%d')
                voteup_count = int(data['voteup_count'])
                author = data['author']['name']
                self.__write('\n'+ content +'\n', author)
                self.__saveToMySQL(question_id, question_name, answer_id, content, date, voteup_count, author)
            if not paging['is_end']:
                self.__continueLoadAnswers(paging['next'], question_id, question_name)
            else:
                return
        else:
            print("服务器链接失败:" + str(result.status_code) + " : " + str(result.reason))
            return

    def __saveToMySQL(self, question_id, question_name, answer_id, content, date, voteup_count, author):
        db = pymysql.connect(host='localhost',user='root', password='yinling2965', port=3306, db='zhihu_spider', charset="utf8")
        cursor = db.cursor()
        data = {
            'keyword': self.__text,
            'question_id': question_id,
            'question_name': question_name,
            'answer_id': answer_id,
            'content': content,
            'date': date,
            'voteup_count': voteup_count,
            'author': author
        }
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=self.__table_name, keys=keys, values=values)
        update = ','.join([" {key} = %s".format(key=key) for key in data])
        sql += update
        try:
            if cursor.execute(sql, tuple(data.values())*2):
                print('Successful')
                db.commit()
        except Exception as e:
            print('Failed:' + str(e))
            db.rollback()
        db.close()

    def __write(self, content, author):
        with open(os.path.join(self.__dirpath, self.__text + ".txt"), 'a+', encoding='utf-8') as f:
            if author is not None:
                f.write("\n**************************"+author+"\n")
            f.write(content)
        f.close()

    # def __findAndDown(self, html, attrs):
    #     # 寻找图片并下载
    #     imglist = BeautifulSoup(html, "html.parser").find_all('img', attrs=attrs)
    #     self.__piclist = []
    #     for img in imglist:
    #         self.__piclist.append(img.get('data-original'))
    #     self.__zhihuPic.doDownload(self.__piclist)
