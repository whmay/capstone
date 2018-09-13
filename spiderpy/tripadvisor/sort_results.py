import sys
import csv

# Read the sight name from file
def get_sight():
	sightArr = []
	with open('sightdata.txt', newline='') as csvfile:
		sightreader = csv.reader(csvfile, delimiter=',')
		for row in sightreader:
			sightArr.append(row[0])
	with open('nophoto.txt', newline='') as csvfile:
		npreader = csv.reader(csvfile, delimiter=',')
		for row in npreader:
			if not row[0] in sightArr:
				sightArr.append(row[0])
	return sightArr

# help/test function
def printDict(dic):
	print(len(dic))
	for keys, values in dic.items():
		print('=======start=========')
		print(keys)
		print(len(values))
		print(values)
		print('========end========')

def read_dict(sightArr):
	# print(len(sightArr))
	# imgDict = {sight:[url,url,url,...] sight:[url,url,url,...] ....}
	imgDict = {}
	for sight in sightArr:
		imgDict.setdefault(sight, [])
	tempkey = 'other'
	with open('results.txt') as fp:
		lines = fp.read().splitlines()
		for line in lines:
			if line in (None, ""): 
				continue
			elif not line.startswith('https'):
				tempkey = line
				if line in imgDict:					
					continue
				else:
					imgDict.setdefault(tempkey, [])
					continue
			elif line in imgDict[tempkey]:
				continue
			else: 
				imgDict[tempkey].append(line)	
	return imgDict


def writeDict(dic):
	with open('imgurls.csv','w',  newline='') as imgcsv:
		fieldnames = ['city/sight','imgurl']
		imgwriter = csv.DictWriter(imgcsv, fieldnames=fieldnames)
		imgwriter.writeheader()
		for keys, values in dic.items():
			for item in dic[keys]:
				imgwriter.writerow({'city/sight': keys, 'imgurl': item})

def main(args):
	sightArr = get_sight()
	print(len(sightArr))
	imgDict = read_dict(sightArr)
	print(len(imgDict))
	writeDict(imgDict)

	with open('compare.csv','w',  newline='') as csvfile:
		writer = csv.writer(csvfile)
		for key in imgDict.keys():
			writer.writerow([key])
		for sight in sightArr:
			writer.writerow([sight])




if __name__ == '__main__':
    from sys import argv
    try:
        main(argv)
    except KeyboardInterrupt:
        pass
    sys.exit()