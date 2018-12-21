import os
import re
import csv
from os import listdir 
from os.path import isfile, join
import random, math
 
# The top argument for walk
path = '/Users/hao/Desktop/testdata/291/291'
 
# The extension to search for
exten = '.jpg'

def rename():
	# add t before name
	for dirpath, dirnames, files in os.walk(topdir):
	    for name in files:
	    	if name.lower().endswith(exten):
	    		oldname = dirpath + "/" +name
	    		newname = dirpath + "/t" + name
	    		os.rename(oldname,newname)
	            # print(os.path.join(dirpath, name))

def renameIndex():
	for dirpath, dirnames, files in os.walk(topdir):
		index = 0
		for name in files:
			if name.lower().endswith(exten):
				oldname = dirpath + "/" + name
				newname = dirpath + "/" + str(index) + exten
				os.rename(oldname,newname)
				index = index+1


def getname():
	dirlist=[]
	for dirpath, dirnames, files in os.walk(topdir):
		# print(dirpath)
		# print(dirnames)
		# print(files)
		for name in dirnames:
			# print(os.path.join(dirpath, name))
			dirlist.append(os.path.join(dirpath, name))
	for item in dirlist:
		print(item)

# Help function to generate the label file
def getlabel():
	dic = {}
	landmarks = [f for f in listdir(path) if not isfile(join(path, f))]
	for key in landmarks:
		dic.setdefault(key, [key])
		imgs = [f for f in listdir(join(path, key)) if not f==".DS_Store"]
		for img in imgs:
			dic[key].append(img)
		dic[key].pop(0)
	
	with open('/Users/hao/Desktop/testdata/291/label.csv','w',  newline='') as sightcsv:
		fieldnames = ['id','landmark']
		sightwriter = csv.DictWriter(sightcsv, fieldnames=fieldnames)
		sightwriter.writeheader()
		for keys, values in dic.items():
			for value in values:
				sightwriter.writerow({'id': value, 'landmark': keys})

# Help function to move test/train data back to one folder
def moveback():
	path1 = '/Users/hao/Desktop/testdata/291/291'
	path2 = '/Users/hao/Desktop/testdata/291/291.1'
	landmarks = [f for f in listdir(path1) if not isfile(join(path1, f))]
	for landmark in landmarks:
		imgs = [f for f in listdir(join(path1, landmark))]
		for item in imgs:
			os.rename(join(join(path1, landmark),item), join(path2, item))

def regrounp():
	path1 = '/Users/hao/Desktop/testdata/291/291.1'
	path2 = '/Users/hao/Desktop/testdata/291/test'
	items = [f for f in listdir(path1)]
	selected = random.sample(items, int(len(items)*0.2))
	for item in selected:
		os.rename(join(path1, item), join(path2, item))

def readtest():
	path2 = '/Users/hao/Desktop/testdata/291/test'
	items = [f for f in listdir(path2)]
	with open('/Users/hao/Desktop/testdata/291/test.csv','w',  newline='') as sightcsv:
		fieldnames = ['id']
		sightwriter = csv.DictWriter(sightcsv, fieldnames=fieldnames)
		sightwriter.writeheader()
		for item in items:
			sightwriter.writerow({'id':item})


if __name__ == '__main__':
	# getlabel()
	# moveback()
	# regrounp()
	readtest()