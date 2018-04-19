from lxml import etree
import os
import pymysql
import csv
import os

path = 'data'
dir = os.listdir(path)

fout = open('midpoint.csv','w')
fout.write('user_id'+','+'user_name'+','+'time'+','+'comment'+','+'shoucang'+','+'zhuanfa'+','+'pinglun'+','+'dianzan'+','+'device'+','+'url\n')


# 创建数据库 (weibo)
def createTable(name):
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
    sql = 'CREATE TABLE IF NOT EXISTS vvvebo (id INT AUTO_INCREMENT NOT NULL,keyword TEXT, user_id TEXT, user_name TEXT, time VARCHAR(255), comment LONGTEXT, shoucang INT, zhuanfa INT, pinglun INT, dianzan INT, device TEXT, url TEXT, PRIMARY KEY(id)) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'
    cursor.execute(sql)
    
    # 允许插入emoil
    #sqldb = 'ALTER DATABASE database_name CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci'
    #sqlta = 'ALTER TABLE table_name CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'
    #sqlcul = 'ALTER TABLE table_name CHANGE column_name column_name VARCHAR(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'

# 插入数据库
def insToDB(data):
    db = pymysql.connect(host='localhost', user='root', password='dadi@1234', port=3306, db='weibo', charset="utf8")
    cursor = db.cursor()
    table = 'vvebo'
    keys = ','.join(data.keys())
    values = ','.join(['%s'] * len(data))
    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
    try:
        if cursor.execute(sql, tuple(data.values())):
            print('插入成功')
            db.commit()
    except:
        print('插入失败')
        db.rollback()
    db.close()
    


# 更新数据库(去重)
def updDB(data):
    table = 'vvebo'
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
    
    

for sub_dir in dir:
    if sub_dir.startswith('.'):
        print('忽略隐藏文件')
    else:
        createTable('weibo')
        sub_path = path + os.sep + sub_dir
        files = os.listdir(sub_path)
        print('Start collecting data from:', sub_path)
        for file in files:
            try:
                file_path = sub_path + os.sep + file 
                fin = open(file_path, mode='r', encoding='unicode_escape')
                source = fin.read().replace('\\','')
                page = etree.HTML(source)
                user_div = page.xpath("//div[@class='WB_cardwrap S_bg2 clearfix']")
                for each in user_div:
                    with open(os.path.join('../keyword.txt'), 'r') as f:
                        keyword = f.read()
                        f.close()
                    mid_div = each.xpath(".//div[@mid]")[0]
                    mid = mid_div.attrib.get('mid')
                    comment_div = each.xpath(".//p[@class='comment_txt']")[0]
                    username = comment_div.attrib.get('nick-name').encode('unicode_escape').decode()
                    comment = etree.tostring(comment_div, method='text', encoding='unicode_escape').decode()
                    time_div = each.xpath(".//div[@class='feed_from W_textb']")[0]
                    time = time_div[1].text if time_div[0].tag != 'a' else time_div[0].text
                    url = time_div[1].attrib.get('href') if time_div[0].tag != 'a' else time_div[0].attrib.get('href')
                    device = time_div[-1].text.encode('unicode_escape').decode()
                    feed_div = each.xpath(".//ul[@class='feed_action_info feed_action_row4']")[0]
                    shoucang = '0' if len(feed_div[0].xpath(".//em"))==0 or feed_div[1].xpath(".//em")[0].text==None else feed_div[0].xpath(".//em")[0].text
                    zhuanfa = '0' if len(feed_div[1].xpath(".//em"))==0 or feed_div[1].xpath(".//em")[0].text==None else feed_div[1].xpath(".//em")[0].text
                    pinglun = '0' if len(feed_div[2].xpath(".//em"))==0 or feed_div[2].xpath(".//em")[0].text==None else feed_div[2].xpath(".//em")[0].text
                    dianzan = '0' if len(feed_div[3].xpath(".//em"))==0 or feed_div[3].xpath(".//em")[0].text==None else feed_div[3].xpath(".//em")[0].text
                    data = (mid+','+username+','+time+','+comment+','+shoucang+','+zhuanfa+','+pinglun+','+dianzan+','+device+','+url).replace('\\t','').replace('\\n','').replace('\\u200b','')
                    fout.write(data+'\n')
                    # 插入数据库
                    dataDic = {
                        'keyword': keyword,
                        'user_id': mid,
                        'time': time,
                        'shoucang': shoucang,
                        'zhuanfa': zhuanfa,
                        'pinglun': pinglun,
                        'dianzan': dianzan,
                        'url': url[2:]
                    }
                    insToDB(dataDic)
                fin.close()
            except Exception as err:
                print ("Something wrong with", file_path,'\n', err)

fout.close()

# rewrite the file, because of the problem about chinese characters encoded by unicode_escape and utf-8
fout = open('final.csv','w', encoding='utf_8_sig')
f = open('midpoint.csv','r',encoding='unicode_escape')
s = f.read()
data = s.split('\n')
for line in data:
    fout.write(line+'\n')
fout.close()


# 读取csv对象 - 更新数据库(comment, device)
csv_file = csv.reader(open('final.csv','r'))
list = []
count = 1    # 去掉第一个
custom_id = 1    
for result in csv_file:
    if count == 1: 
        count += 1 
        continue;
    if len(result) > 9:
        data = {
            'id': custom_id,
            'user_name': result[1],
            'comment': result[3],
            'device': result[8]
        }
        updDB(data)
        custom_id += 1

        
        
        
        
        