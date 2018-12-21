import urllib.request 
from socket import timeout
from bs4 import BeautifulSoup  # 解析网页内容
#import tqdm
from urllib import request, error
from PIL import Image
from io import BytesIO
import os
import csv

def parse_data(data_file):
    csvfile = open(data_file, 'r')
    csvreader = csv.reader(csvfile)
    key_url_list = [line[:2] for line in csvreader]
    return key_url_list[1:]  # Chop off header

def download_image(directory,key_url):
    out_dir = directory
    #out_dir = directory + '/'
    (key, url) = key_url
    filename = os.path.join(out_dir, '{}.jpg'.format(key))
    #url = 'https://mdn.mozillademos.org/files/12634/sw-fetch.png'
    #print(url)

    if os.path.exists(filename):
        print('Image {} already exists. Skipping download.'.format(filename))
        return 0

    try:
        print("1.0 response")
        response = request.urlopen(url,timeout=10)
        image_data = response.read()
        print("1 get response")
    except:
        print('Warning: Could not download image {} from {}'.format(key, url))
        return 1

    try:
        pil_image = Image.open(BytesIO(image_data))
        print("2 get img")
    except:
        print('Warning: Failed to parse image {}'.format(key))
        return 1

    try:
        pil_image_rgb = pil_image.convert('RGB')
        print("3 get rgb")
    except:
        print('Warning: Failed to convert image {} to RGB'.format(key))
        return 1

    try:
        pil_image_rgb.save(filename, format='JPEG', quality=90)
        print("4 get save")
    except:
        print('Warning: Failed to save image {}'.format(filename))
        return 1
    
    return 0


# if __name__ == '__main__':
# 	with open('/Users/hao/Desktop/spiderpy/sample.csv', newline='') as csvfile:
# 		reader = csv.DictReader(csvfile)
# 		index = 0
# 		failures = 0
# 		for row in reader:
# 			directory = '/Users/hao/Desktop/spiderpy/small' + row['city/sight']
# 			if not os.path.exists(directory):
# 				os.makedirs(directory)
#             index = index + 1
#             name = "g"+str(index)
#             key_url = (name, row['imgurl'])
# 			failures = failures + download_image(directory,key_url)

#         print('Total number of download failures:', failures)	


if __name__ == '__main__':
    with open('/Users/hao/Desktop/data/googleImg.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        index = 0
        failures = 0
        for row in reader:
            directory = '/Users/hao/Desktop/data/dataset/' + row['city/sight']
            if not os.path.exists(directory):
                os.makedirs(directory)
            index = index + 1
            print(index)
            name = "g"+str(index)
            key_url = (name, row['imgurl'])
            failures = failures + download_image(directory,key_url)
    print('Total number of download failures:', failures)   



