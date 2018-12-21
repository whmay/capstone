
import urllib.request 
from bs4 import BeautifulSoup  # 解析网页内容
from urllib.parse import  urljoin  # Absolute URL
import re                      # 正则式模块.
import os                      # 系统路径模块: 创建文件夹用
import socket                  # 下载用到?
import time                    # 下载用到?
import csv


base_url = 'http://you.ctrip.com'
cities = ['hangzhou14','shanghai2','chengdu104','xiamen21','taipeicity360',
		   'hongkong38','beijing1','suzhou11','nanjing9','lijiang32','chongqing158',
		   'wuhan145','kunming29','guangzhou152','tianjin154','shenzhen26','macau39',
		   'wuxi10','dali31','dalian4','changsha148','ningbo83','shenyang155','guilin28',
		   'xian7','xishuangbanna30','haerbin151','zhangjiajie23','lhasa36','gaoxiong756',
		   'sanya61','yangzhou12','qingdao5','hualien1366','xianggelila106','fenghuang988',
		   'beihai140','shaoxing18','guiyang33','aba744','fuzhou164','xining237','yangshuo702',
		   'xiangxi496','qinhuangdao132','changchun216','jiuzhaigou25','weihai169','jinan128',
		   'zhuhai27','emeishan24','haikou37','wuyishan22','zhoushan479','taiyuan167',
		   'zhengzhou157','yinchuan239','jiaxing272','leshan103']

dic = {}   # city/sight : sighturl
dic2 = {}  # city/sight : a list of image urls

for city in cities:
	print(city)
	cities_url = urljoin(base_url, '/place/' + city + '.html')
	print(cities_url)
	
	resp = urllib.request.urlopen(cities_url)
	sauce = resp.read()

	soup = BeautifulSoup(sauce, "lxml")

	# There are two divs belong to footerseo_con seojs3line classes, 
	# the first one is we need.
	# Read the city/sight and the according url to a dictionary
	divTag = soup.find_all('div',{'class':'footerseo_con seojs3line'})
	for div in divTag:
		links = div.find_all('a')
		for sight in links:
			sight_url = urljoin(base_url, sight.get('href'))
			dic[city + '/' + sight.text] = sight_url
		break

# delete the incorrect value
dic = {key:val for key, val in dic.items() if val != 'javascript:;'}
for keys, values in dic.items():
	print(keys)
	print(values)
print(len(dic))

# write the dictonary to a csv file
with open('/Users/hao/Desktop/data/sight_url.csv','w',  newline='') as sightcsv:
	fieldnames = ['city/sight','url']
	sightwriter = csv.DictWriter(sightcsv, fieldnames=fieldnames)
	sightwriter.writeheader()
	for keys, values in dic.items():
		sightwriter.writerow({'city/sight': keys, 'url': values})

# get the image url
with open('/Users/hao/Desktop/data/sight_url.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		key = row['city/sight']
		dic2.setdefault(key, [key])
		sight_url = row['url']
		resp = urllib.request.urlopen(sight_url)
		sauce = resp.read()
		soup = BeautifulSoup(sauce, "lxml")
		num_comments = soup.find_all('li',{'class':'comment_piclist'})
		for comment in num_comments:
			img_links = comment.find_all('a')
			for img_link in img_links:
				dic2[key].append(img_link.get('href'))
		
print(len(dic2))

# write the image url to the file
with open('/Users/hao/Desktop/data/image_url.csv','w',  newline='') as imgcsv:
	fieldnames = ['city/sight','imgurl']
	imgwriter = csv.DictWriter(imgcsv, fieldnames=fieldnames)
	imgwriter.writeheader()
	for keys, values in dic2.items():
		for item in dic2[keys]:
			imgwriter.writerow({'city/sight': keys, 'imgurl': item})
		
