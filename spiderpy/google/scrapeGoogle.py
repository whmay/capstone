from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import urllib.parse
import requests
import re
import os
import argparse
import sys
import json
import csv

# adapted from http://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search

def get_soup(url,header):
	req =  Request(url, headers= header)
	sauce = urlopen(req).read()
	soup = BeautifulSoup(sauce, "lxml")
	return soup

# Read the sight name from file
def get_sight():
	sightArr = []
	with open('sight_url.csv', newline='') as csvfile:
		sightreader = csv.reader(csvfile, delimiter=',')
		for row in sightreader:
			sightArr.append(row[0])
	return sightArr

# help/test function
def printDict(dic):
	for keys, values in dic.items():
		print(keys)
		print(values)

# write the sight and according image urls to the file
def writeCsv(dic):
	with open('googleImgtestCtrip.csv','w',  newline='') as imgcsv:
		fieldnames = ['city/sight','imgurl']
		imgwriter = csv.DictWriter(imgcsv, fieldnames=fieldnames)
		imgwriter.writeheader()
		for keys, values in dic.items():
			for item in dic[keys]:
				imgwriter.writerow({'city/sight': keys, 'imgurl': item})

def main(args):
	sightArr = get_sight();
	# imgDict = {sight:[url,url,url,...] sight:[url,url,url,...] ....}
	imgDict = {}
	header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

	for sight in sightArr:
		imgDict.setdefault(sight, [])
		print(sight)
		query = urllib.parse.quote(sight)
		url = "https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
		soup = get_soup(url,header)
		for a in soup.find_all("div",{"class":"rg_meta"}):
			try:
				link =json.loads(a.text)["ou"]
			except:
				print("Unexpected error:", sys.exc_info()[0])
			imgDict[sight].append(link)

	writeCsv(imgDict)
	

if __name__ == '__main__':
    from sys import argv
    try:
        main(argv)
    except KeyboardInterrupt:
        pass
    sys.exit()