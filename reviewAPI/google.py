# read 1000 urls from train.csv
import argparse
import io

from google.cloud import vision

def load():
	import pandas as pd 
	rawdata = pd.read_csv("train.csv", nrows = 500)
	data = rawdata["url"]
	return data

# [START def_detect_landmarks_uri]
def detect_landmarks_uri(uri):
    """Detects landmarks in the file located in Google Cloud Storage or on the
    Web."""
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    if landmarks:
    	print ('++++++landmark detected++++++')
    	for landmark in landmarks:
    		print(landmark.description)
    	return 1
    else: 
    	print ('???unknown???')
    	return 0

# [END def_detect_landmarks_uri]

if __name__ == '__main__':
	i = 0
	data = load()
	for uri in data:
		i = i + detect_landmarks_uri(uri)
	print(i)

