import urllib.request, urllib.parse, datetime
from bs4 import BeautifulSoup


# 创建文件夹函数，可要可不要
def mkdir(path):
    import os
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


# 定义写入器，操作记录文件
def writter(mkpath, towrite):
    towrite_file = open(mkpath + "result.txt", 'a')
    towrite_file.write(towrite)
    towrite_file.close()


# 保存路径
# mkpath = "c:\\weatherdata\\"
mkpath = "/tmp/weatherdata/"
mkdir(mkpath)
# 构造header
page_head_url = "http://www.tianqihoubao.com/lishi/tianjin/month/"
ua_header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Mobile Safari/537.36'}
# 生成年月列表yymmlist，从2011年1月到当前年月
yymmlist = []
for i in range(2011, datetime.datetime.now().year + 1):
    if i == datetime.datetime.now().year:
        monthrange = datetime.datetime.now().month + 1
    else:
        monthrange = 12 + 1
    for j in range(1, monthrange):
        if j < 10:
            yymmlist.append(str(i) + "0" + str(j))
        else:
            yymmlist.append(str(i) + str(j))
# 遍历年月列表并生成对应url
for page_num in yymmlist:
    # 获取该页源码
    page_url = page_head_url + str(page_num) + ".html"
    try:
        request = urllib.request.Request(page_url, headers=ua_header)
        response = urllib.request.urlopen(request, timeout=30)
    except:
        print(str(page_num) + "页连接失败")
        continue
    page_source_code = str(response.read(), encoding="gb2312")
    soup = BeautifulSoup(page_source_code, features="lxml")
    # 记录页码日志
    print("正在搜索" + str(page_num) + "页")
    page_table = soup.findAll(attrs={"class": "b"})
    tds = []
    for td in page_table[0].findAll('td'):
        tds.append(str(td.getText()).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', ''))
    del tds[0:4]
    count = 1
    for towrite in tds:
        if count % 4 != 0:
            writter(mkpath, towrite + ",")
        else:
            writter(mkpath, towrite + "\n")
        count = count + 1
