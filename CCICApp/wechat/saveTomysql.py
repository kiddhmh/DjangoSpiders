import pymysql


# 创建表
def createTable():
	db = pymysql.connect(host='localhost', user='root', password='dadi@1234', port=3306)
	cursor = db.cursor()
	# 判断数据库是否存在
	result = cursor.execute('SHOW DATABASES LIKE "weibo"')
	if result == 0:
		cursor.execute('CREATE DATABASE weibo DEFAULT CHARACTER SET utf8mb4 COLLATE = utf8mb4_unicode_ci')
		db.close()
	# 创建表
	db = pymysql.connect(host='localhost', user='root', password='dadi@1234', port=3306, db='weibo')
	cursor = db.cursor()
	sql = 'CREATE TABLE IF NOT EXISTS wechat (id INT AUTO_INCREMENT NOT NULL,keyword TEXT, article_title TEXT, article_url TEXT, article_imgs TEXT, article_abstract TEXT, article_time TEXT, gzh_profile_url TEXT, gzh_headimage TEXT, gzh_wechat_name TEXT, gzh_isv INT, PRIMARY KEY(article_title)) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'
	cursor.execute(sql)
	
	
	

# 更新数据库(去重)
def insertToDB(data):
	table = 'wechat'
	keys = ', '.join(data.keys())
	values = ', '.join(['%s'] * len(data))
	db = pymysql.connect(host='localhost', user='root', password='dadi@1234', port=3306, db='weibo', charset="utf8")
	cursor = db.cursor()
	sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys, values=values)
	update = ','.join([" {key} = %s".format(key=key) for key in data])
	sql += update
	try:
		if cursor.execute(sql, tuple(data.values())*2):
			print('更新成功')
			db.commit()
	except Exception as err:
		print('更新失败', err)
		db.rollback()
	db.close()