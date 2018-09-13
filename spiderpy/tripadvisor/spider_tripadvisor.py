# Download top 60 of 60 cities popular sights url from tripadvisor.Save them to the sight_url_tripadvisor.csv file.

import urllib.request 
from bs4 import BeautifulSoup  # 解析网页内容
from urllib.parse import  urljoin  # Absolute URL
import csv

base_url = 'https://www.tripadvisor.com/'
tail_url = '.html#ATTRACTION_SORT_WRAPPER'
tail_url_page2 = '.html#FILTERED_LIST'
# 60 cities * 60 sights
cities = ['g294217-Hong_Kong','g294212-Beijing','g308272-Shanghai','g664891-Macau','g297463-Chengdu_Sichuan',
			'g298555-Guangzhou_Guangdong','g298557-Xi_an_Shaanxi','g303783-Lijiang_Yunnan','g298559-Hangzhou_Zhejiang','g297442-Suzhou_Jiangsu',
			'g297415-Shenzhen_Guangdong','g294213-Chongqing','g294220-Nanjing_Jiangsu','g297437-Wuhan_Hubei','g311293-Tianjin',
			'g297407-Xiamen_Fujian','g297458-Qingdao_Shandong','g297454-Shenyang_Liaoning','g297452-Dalian_Liaoning','g297433-Harbin_Heilongjiang',
			'g298558-Kunming_Yunnan','g297435-Zhengzhou_Henan','g297412-Dongguan_Guangdong','g494932-Changsha_Hunan','g297457-Jinan_Shandong',
			'g297427-Sanya_Hainan','g494927-Foshan_Guangdong','g303781-Dali_Yunnan','g297470-Ningbo_Zhejiang','g297443-Wuxi_Jiangsu',
			'g297448-Changchun_Jilin','g297403-Hefei_Anhui','g317092-Nanning_Guangxi','g297405-Fuzhou_Fujian','g298556-Guilin_Guangxi',
			'g297446-Nanchang_Jiangxi','g297430-Qinhuangdao_Hebei','g317090-Guiyang_Guizhou','g317093-Taiyuan_Shanxi','g297418-Zhuhai_Guangdong',
			'g297431-Shijiazhuang_Hebei','g297466-Urumqi_Xinjiang_Uygur','g658407-Zhoushan_Zhejiang','g656832-Changzhou_Jiangsu','g297425-Haikou_Hainan',
			'g494933-Zhangjiajie_Hunan','g303712-Yangshuo_County_Guangxi','g1158709-Jiashan_County_Zhejiang','g297417-Zhongshan_Guangdong','g297409-Lanzhou_Gansu',
			'g294223-Lhasa_Tibet','g297420-Beihai_Guangxi','g303731-Luoyang_Henan','g494940-Xining_Qinghai','g303685-Huangshan_Anhui',
			'g641713-Yantai_Shandong','g297440-Hohhot_Inner_Mongolia','g297472-Wenzhou_Zhejiang','g494934-Yangzhou_Jiangsu','g679674-Zibo_Shandong']
dic = {} # city/sight:url

for city in cities:
	city = city.split('-')
	cityhead = city[0]
	citytail = city[1]
	city_url = urljoin(base_url, 'Attractions-' + cityhead + '-Activities-' + citytail + tail_url)
	# Page 2
	city_url2 = urljoin(base_url, 'Attractions-' + cityhead + '-Activities-oa30-' + citytail + tail_url_page2)

	# 60 sights in 2 pages
	# first page
	resp = urllib.request.urlopen(city_url)
	sauce = resp.read()
	soup = BeautifulSoup(sauce, "lxml")

	divTag = soup.find_all('div',{'class':'listing_title'})
	for div in divTag:
		sight = div.find('a')
		sight_url = urljoin(base_url, sight.get('href'))
		dic[citytail+'/'+sight.text] = sight_url

	# next page
	resp = urllib.request.urlopen(city_url2)
	sauce = resp.read()
	soup = BeautifulSoup(sauce, "lxml")

	divTag = soup.find_all('div',{'class':'listing_title'})
	for div in divTag:
		sight = div.find('a')
		sight_url = urljoin(base_url, sight.get('href'))
		dic[citytail+'/'+sight.text] = sight_url
  
# remove tours, shops
for key in list(dic.keys()):
	if 'Tours' in key:
		del dic[key]
	elif 'Shops' in key:
		del dic[key]
	else: continue

# for keys, values in dic.items():
# 	print(keys)
# 	print(values)
# print(len(dic))


with open('/Users/hao/Desktop/data/sight_url_tripadvisor.csv','w',  newline='') as sightcsv:
	fieldnames = ['city/sight','url']
	sightwriter = csv.DictWriter(sightcsv, fieldnames=fieldnames)
	sightwriter.writeheader()
	for keys, values in dic.items():
		sightwriter.writerow({'city/sight': keys, 'url': values})

