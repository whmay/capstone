This is a capstone project. It follows a typical machine learning process, from data collection, preparation to model training, evaluation, to integration to an iOS application. 
Technicals used here includes: web scraping, deep learning with convolutional neural network, transfer learning, iOS application development. 
Tools used here includes: Python, Node.js, Swift, Google Colaboratory, Azure virtual machine.


---------------------------------------------------------------------------------
--------------Folder: dataset----------------------------------------------------
Chinese landmark & attraction dataset
1. The image dataset (10.3G) is shared via one drive from this link
https://1drv.ms/f/s!AmBHBOsyDMiaofUKRWvysLrL5kGClA password:landmark

2. The raw image landmark dataset (89.2G) is shared via one drive from this link
https://1drv.ms/f/s!AmBHBOsyDMiapP4tcrsqldy8a-1rPA password:landmark

3. landmark.csv
landmark_id, number of images for each landmark.

4. lanmarknames.txt
Landmark names.
---------------------------------------------------------------------------------
--------------Folder:Reprot&ppt--------------------------------------------------
1. Chinese Landmark & Attraction Recognition.pdf
Project report

2. HaoWu.ppt
The defense presentation
---------------------------------------------------------------------------------
--------------Folder:model-------------------------------------------------------
1. landmark.py
The script used to train & evaluate CNN models

2. landmark.ipynb
Google colaboratory file for train & evaluate CNN models.
---------------------------------------------------------------------------------
--------------Folder:WebScraping-------------------------------------------------
1. spiderCtrip.py
Contains functions used for web scraping Ctrip.

2. spider_tripadvisor.py
   getsrc.js
Contains functions used for web scraping tripadvisor.

3. scrapeGoogle.py
Contains functions used for web scraping Google Image search.

4. download.py
Contains functions used for downloading images.
---------------------------------------------------------------------------------
--------------Folder:Imagecluster------------------------------------------------
1. imagecluster folder
Pycharm project used for image clustering.

Credits: Steve Schmerler https://github.com/elcorto/imagecluster
---------------------------------------------------------------------------------
--------------Folder:Delf--------------------------------------------------------
1. delf folder 
Python project used for image cropping.
Credits: Noh, Hyeonwoo, et al. "Large-Scale Image Retrieval with Attentive Deep Local Features." Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition. 2017.
---------------------------------------------------------------------------------
--------------Other help function------------------------------------------------
1. dataexpl.py
Contains functions used for database analysis, iterate image clustering results, etc.

2. help.py
Contains functions used for group, rename, index the images.

---------------------------------------------------------------------------------
--------------iOS application----------------------------------------------------
1. TourChina folder
Xcode project for TourChina application
Readme file included.
Credits: Shawon Ashraf https://github.com/ShawonAshraf/Frutify-iOS
---------------------------------------------------------------------------------