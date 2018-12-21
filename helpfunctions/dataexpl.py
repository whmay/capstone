import os,glob
import csv
import random
from os import listdir 
from os.path import isfile, join

from PIL import Image
import random, math
import shutil

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns


path = "/Users/hao/Desktop/testdata/414/Nolandmark"
spath = "/Users/hao/Desktop/testdata/CNLandmark"
p1 = "/Users/hao/Desktop/testdata/6sixth/test"
p2 = "/Users/hao/Desktop/testdata/6sixth/train"
p3 = "/Users/hao/Desktop/testdata/6sixth/test1"
p4 = "/Users/hao/Desktop/testdata/414/t"

def showThumbnails(list):	
	print("Number of the show list: " + str(len(list)))
	row = math.ceil((math.sqrt(len(list))))
	print("Number of row: " + str(row))
	width = (row)*300
	new_img = Image.new("RGB",(width,width))
	index = 0
	for i in range(0,width,300):
		for j in range(0,width,300):
			try:
				im = Image.open(list[index])
			except IndexError:
				break
			index += 1
			im.thumbnail((300,300))
			new_img.paste(im,(i,j))
	new_img.save('test.jpg')
	img = Image.open('test.jpg')
	img.show()
	img.close()

# rename the image with the landmark id and index
# write the image, landmark id and landmark name to a csv file
def getLandmarkList():
	dataset = []
	landmarks = [f for f in listdir(path) if not isfile(join(path, f))]
	landmark_id = 0
	for landmark in landmarks:
		landmark_id += 1
		imgs = [f for f in listdir(join(path, landmark)) if not f==".DS_Store"]
		img_index = 0
		print(len(imgs))
		for img in imgs:
			old = join(join(path, landmark), img)
			# print(old)
			new = str(landmark_id) +"_"+str(img_index)+".jpg"
			data = [new, landmark_id, landmark]
			dataset.append(data)
			img_index += 1
			os.rename(old, join(join(path, landmark), new))

	with open("CNLandmark.csv","w", newline="") as imgcsv:
		fieldnames = ["img", "landmark_id", "landmark"]
		imgwriter = csv.DictWriter(imgcsv, fieldnames=fieldnames)
		imgwriter.writeheader()
		for item in dataset:
			imgwriter.writerow({"img":item[0], "landmark_id":item[1], "landmark":item[2]})

# data exploration 
def analysis1():
	data_df = pd.read_csv("CNLandmark.csv")
	print("Landmark dataset data shape -  rows:",data_df.shape[0]," columns:", data_df.shape[1])
	print(data_df.nunique())
	
	# Landmark id distribuition and density plot
	plt.figure(1, figsize=(8,8))
	plt.title('Landmark id density plot')
	sns.kdeplot(data_df['landmark_id'], color="tomato", shade=True)

	plt.figure(2, figsize = (8, 8))
	plt.title('Landmark id distribution and density plot')
	sns.distplot(data_df['landmark_id'],color='green', kde=True,bins=100)
	
	plt.show()

	# the most frequent landmark occurences
	th10 = pd.DataFrame(data_df.landmark_id.value_counts().head(10))
	th10.reset_index(level=0, inplace=True)
	th10.columns = ['landmark_id','count']
	print(th10)

	# the least frequent landmark occurences
	tb10 = pd.DataFrame(data_df.landmark_id.value_counts().tail(10))
	tb10.reset_index(level=0, inplace=True)
	tb10.columns = ['landmark_id','count']
	print(tb10)

def analysis():
	labels = ["Ancient Bridge", "Ancient Town", "Bell and drum Tower", "Campus","Canal Town","Church=religion", "City bird view", "Decorated Archway", "Entrance", "Former Residence", "Garden","GreatWall", "Hall", "Island" ,"Lake" ,"Mall","Modern Bridge" ,"Modern Building" ,"Mountain" ,"Other" ,"Park","Railway Station" ,"River","Rock" ,"Seaside" ,"Skyscraper" ,"Snow Mountain" ,"Stature" ,"Street" ,"Temple","Theme Park","Tomb","Tower" ,"Town","Waterfall"]
	x = np.arange(34)
	data_df = pd.read_csv("info.csv")
	y1 = data_df['num of landmark'].astype("int")
	# plt.style.use('ggplot')
	# plt.xticks(x, labels)
	# plt.xticks(rotation=80)
	# plt.ylabel("Number of Landmarks")
	# y2 = data_df['num of images'].astype("int")
	# plt.bar(x, y1)
	# plt.show()
	# plt.close()

	df = pd.read_csv("ldick1.csv")
	plt.style.use('ggplot')
	y = df["number of images"].astype("int")
	plt.plot(y)
	plt.xlabel("Landmark id")
	plt.ylabel("Number of Images")
	plt.show()
	plt.close()


# get popular landmarks to other folders
def popular():
	data_df = pd.read_csv("CNLandmark.csv")
	popular_landmarks = []
	id_frequency= data_df["landmark_id"].value_counts().to_dict()
	for key, value in id_frequency.items():
		if value > 100:
			popular_landmarks.append(key)
	print(popular_landmarks)
	print(len(popular_landmarks))

	for landmark_id in popular_landmarks:
		os.rename(join(path, str(landmark_id)), join(spath, str(landmark_id)) )

def printDict(dic):
	for keys, values in dic.items():
		print(keys)
		print(values)

# rename the landmark folders with landmark id
def rename():
	landmark_dict = {}
	with open("CNLandmark.csv","r", newline="") as csvfile:
		reader = csv.reader(csvfile, delimiter=",")
		for row in reader:
			landmark_dict[row[2]] = row[1]
	landmark_dict.pop("landmark")
	
	# printDict(landmark_dict)

	landmarks = [f for f in listdir(path) if not isfile(join(path, f))]
	for landmark in landmarks:
		landmark_id = landmark_dict[landmark]
		print(join(path,landmark) )
		print(join(path,landmark_id))
		os.rename(join(path,landmark), join(path,landmark_id))

#  make all the data into two groups, 80% for train data, 20% for test data
def regroup():
	# with open("6sixth/labels.txt") as f:
	# 	landmarks = f.read().splitlines()
	landmarks = [f for f in listdir(path) if not isfile(join(path, f))]
	for landmark in landmarks:
		if not os.path.exists(join(p4, landmark)):
			os.makedirs(join(p4, landmark))
		print("landmark:" + landmark)
		imgs = [f for f in listdir(join(path, landmark))]
		selected = random.sample(imgs, int(len(imgs)*0.2))
		for item in selected:
			print("item" + item)
			os.rename(join(join(path, landmark),item), join(join(p4, landmark),item))
		

def show():
	labels = [0,"Ancient Bridge", "Ancient Town", "Bell and drum Tower", "Campus","Canal Town","Church=religion", "City bird view", "Decorated Archway", "Entrance", "Former Residence", "Garden","GreatWall", "Hall", "Island" ,"Lake" ,"Mall","Modern Bridge" ,"Modern Building" ,"Mountain" ,"Other" ,"Park","Railway Station" ,"River","Rock" ,"Seaside" ,"Skycraper" ,"Snow Mountain" ,"Stature" ,"Street" ,"Temple","Theme Park","Tomb","Tower" ,"Town","Waterfall"]
	# key(id) : values([lenght of imgs, number of features, tags])
	# int:list[int, int, str, str, ....]
	ldict={}
	landmarks = [f for f in listdir(spath) if not isfile(join(spath, f))]
	for landmark in landmarks:
		print("*********************************")
		print("Landmark id is: " + str(landmark))
		thumbList = []
		ldict[int(landmark)] = []
		tags = []
		imgs = [f for f in listdir(join(spath, landmark)) if not f==".DS_Store"]
		print("Number of images: " + str(len(imgs)))
		ldict[int(landmark)].append(len(imgs))
		select = 1+int(len(imgs)*0.2)
		selected = random.sample(imgs, select)
		for img in selected:
			thumbList.append(join(join(spath, landmark),img))
		showThumbnails(thumbList)

		numOfFeatures = input("number of features: ").split()[0]
		ldict[int(landmark)].append(int(numOfFeatures))
		index = input("tag: ").split()
		for i in index:
			ldict[int(landmark)].append(labels[int(i)])

	with open('ldick.csv','a',  newline='') as lcsv:
		fieldnames = ["landmark_id","number of images", "number of features", "labels"]
		lwriter = csv.DictWriter(lcsv, fieldnames=fieldnames)
		lwriter.writeheader()
		for keys, values in ldict.items():
			lwriter.writerow({"landmark_id": keys, "number of images":values[0], "number of features":values[1], "labels":values[2:]})


if __name__ == '__main__':
	# getLandmarkList()
	# analysis()
	# rename()
	regroup()
	# show()
	# with open("500.txt") as f:
	# 	name = f.readlines()
	# print(name)
	# landmarks = [f for f in listdir(spath) if not isfile(join(path, f))]
	# for landmark in landmarks:
	# 	print(landmark)
