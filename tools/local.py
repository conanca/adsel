#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''抓取 国家统计局网站 上的最新县及县以上行政区划代码，并保存成 json 格式的js文件
by Conanca
'''

import urllib2,json

url_prefix = 'http://www.stats.gov.cn/tjbz/xzqhdm/'

var_text = 'xzqh'
code_text = 'C'
name_text = 'N'
sub_text = 'S'
file_path = 'xzqh.js'

def set_proxy(proxy):
    ''' 设置代理服务器 '''
    urllib2.install_opener(urllib2.build_opener(urllib2.ProxyHandler({'http' : proxy})))

def get_latest_page():
    ''' 获取最新的行政区划代码公布页 '''
    content = urllib2.urlopen(url_prefix + 'index.htm').read()
    index_start = content.find("<td width='76%' height='20' valign='middle'><a href='") + 53
    index_end = content.find("' target='_blank'  class='a2'>")
    xzqhdm_url = content[index_start:index_end]
    xzqhdm_url = url_prefix + xzqhdm_url
    print 'latest page:' + xzqhdm_url
    return xzqhdm_url

def crawl_page(xzqhdm_url):
    ''' 爬行政区划代码公布页 '''
    print 'crawling...'
    content = urllib2.urlopen(xzqhdm_url).read()
    index_start = content.find('''<td class='content'><span class="content">''') + 42
    index_end = content.find("<BR></span></td>")
    content = content[index_start:index_end]
    # print content
    return content

def convert(content):
    ''' 将爬到的内容转换为行政区划 list '''
    print 'converting...'
    item_arr = content.replace('&nbsp;','*').split('<BR>')
    p_list = []
    current_p = {}
    current_p_sub = []
    current_c = {}
    current_c_sub = []
    current_d = {}
    for item_str in item_arr:
        #print item_str
        if item_str.count('*')==1:
            print 'got a province:'+item_str
            if len(current_p)!=0:
                # 为当前省 设置其子项;省列表中添加当前省
                current_p[sub_text] = current_p_sub
                p_list.append(current_p)
            # 赋值 当前省;初始化 当前省的子项
            current_p = creat_item(item_str)
            current_p_sub = []
        elif item_str.count('*')==3:
            print '********got a city:'+item_str
            # 赋值 当前市;初始化 当前市的子项
            current_c = creat_item(item_str)
            current_c_sub = []
            if len(current_c)!=0:
                # 为当前市 设置其子项;当前省的子项中添加当前市
                current_c[sub_text] = current_c_sub
                current_p_sub.append(current_c)
        elif item_str.count('*')>=5:
            print '****************got a district:'+item_str
            # 赋值 当前区县;当前市的子项中添加当前区县
            current_d = creat_item(item_str)
            current_c_sub.append(current_d)
        else :
            print 'invaild item string:'+item_str
    return p_list

def creat_item(item_str):
    ''' 根据字符串创建条目对象 '''
    t = item_str.split(' ')
    code = t[0].replace('*','')
    name = t[1].replace('*','')
    item = {code_text:code,name_text:name}
    #print item
    return item

def write_to(content,file_path):
    ''' 将行政区划列表写入指定的js文件中 '''
    print 'writing...'
    f = open(file_path, 'w')
    f.write('var {0}={1}'.format(var_text,content))
    f.close()
    print 'finished!'
   
if __name__ == '__main__':
    #set_proxy('http://192.168.2.61:8080')
    url = get_latest_page()
    content = crawl_page(url)
    p_list = convert(content)
    content = json.dumps(p_list,ensure_ascii=False,separators=(',',':')).decode('gb18030').encode('utf-8')
    write_to(content,file_path)
