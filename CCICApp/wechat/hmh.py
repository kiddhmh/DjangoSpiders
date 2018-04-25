import wechatsogou
import saveTomysql
import time

# 可配置参数

# 直连
ws_api = wechatsogou.WechatSogouAPI()

# 验证码输入错误的重试次数，默认为1
ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=3)


# 所有requests库的参数都能在这用
# 如 配置代理，代理列表中至少需包含1个 HTTPS 协议的代理, 并确保代理可用
ws_api = wechatsogou.WechatSogouAPI(proxies={
	"http": "10.1.27.102:8080",
	"https": "10.1.27.102:8080",
})

# 如 设置超时
ws_api = wechatsogou.WechatSogouAPI(timeout=30)


# 搜索微信公众号文章
# result = ws_api.search_article('大地保险', page=10)
keyword = input('请输入查询关键字: ')
if keyword == '':
	print('关键字不能为空')
else:
	results = ws_api.search_all(keyword)
	if len(results) == 0:
		print('未搜索到相关文档')
	else:
		# 插入数据库
		saveTomysql.createTable()
		for result in results:
			# 时间戳转化为时间
			timeLine = result['article']['time']
			time_local = time.localtime(timeLine)
			dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
			imgs = result['article']['imgs']
			images = ''
			if len(imgs) != 0:
				images = ' , '.join('%s' %idd for idd in imgs)
				
			data = {
				'keyword': keyword,
				'article_title': result['article']['title'],
				'article_url': result['article']['url'],
				'article_imgs': images,
				'article_abstract': result['article']['abstract'],
				'article_time': dt,
				'gzh_profile_url': result['gzh']['profile_url'],
				'gzh_headimage': result['gzh']['headimage'],
				'gzh_wechat_name': result['gzh']['wechat_name'],
				'gzh_isv': result['gzh']['isv']
			}
			saveTomysql.insertToDB(data)



