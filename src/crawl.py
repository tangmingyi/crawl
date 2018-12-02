from bs4 import BeautifulSoup
import requests
import re
'''
处理步骤
    1：获取文章的url（网页上通常都有文章链接的索引集，获取这个集合，组成url集）
    2：利用正则表达式筛选掉一些不是html的索引页
    3：爬取剩下网页的新闻内容
'''
pattern = "//[^\s]*.shtml"          #这是正则表达的pattern，目的是只获取.shtml后缀的url
url = 'http://sports.sina.com.cn/'  #爬取的起始页

web_data = requests.get(url)        
web_data.encoding = 'utf-8'
soup = BeautifulSoup(web_data.text,'lxml')  #beautifulSoup是解析网页的工具，很好用
list_context = soup.select('.tianyi__wrap-a')
a_list = list_context[0].select('a')
links = list()
for a_tag in a_list:
    link = a_tag["href"]
    result = re.search(pattern,link)
    if result != None:
        links.append("http:" + link)


count = 0           #记录成功爬取的文件数目
write_file = open("../data/result.txt", "w", encoding="utf-8")
write_file_analy = open("../data/analy_links.txt", "w", encoding="utf-8")
for link in links:
    web_data = requests.get(link)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text,'lxml')
    list_context = soup.select('.article')
    if len(list_context) > 0:
        count = count +1
        p_tag = list_context[0].select('p')
        for a in p_tag:
            write_file.write(a.text)
            write_file.write("\n")
    else:
        write_file_analy.write(link)
        write_file_analy.write("\n")
write_file.close()
write_file_analy.close()
print(count)

