import csv

dic = {}

with open('./testdata.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		key = row['city/sight']
		dic.setdefault(key, [key])
		sight_url = row['url']
		dic[key].append(sight_url)


for keys, values in dic.items():
	print(keys)
	print(values)