import urllib
from BeautifulSoup import *
import re
import os
from threading import Thread

#List of yelp urls to scrape
url='http://www.yelp.com/biz/c-level-san-diego'
directoryForDB = "/Users/jessicazhao/Documents/homework/CC"
if not os.path.exists(directoryForDB):
	os.makedirs(directoryForDB)
i=0
#function that will do actual scraping job
f1=open("./html.txt","w")
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)
title = soup.find('h1',itemprop="name")
saddress = soup.find('span',itemprop="streetAddress")
postalcode = soup.find('span',itemprop="postalCode")
print >>f1,soup
