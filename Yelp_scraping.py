import csv
import urllib
from BeautifulSoup import *
import re
import os
from threading import Thread


#read business list for bizID
bizfilePath="/Users/jessicazhao/Documents/workspace-java/yelpAPI/data/biz-1.csv"
fhand=urllib.urlopen(bizfilePath)
bizURL=dict()#key:bizid  value:bizURL
try:
    reader=csv.reader(fhand)
    next(reader,None)
    for row in reader:
        bizURL[row[0]]="http://www.yelp.com/biz/"+row[0]
        
finally:
    fhand.close()
    
reviewBiz=dict()#key:reviewid  value:bizid
reviewUser=dict()#key:reviewid value:userid
reviewStar=dict()#key:reviewid  value:rating
reviewUseful=dict()#key:reviewid  value:votes count(useful)
reviewFunny=dict()#key:reviewid  value:votes count(funny)
reviewCool=dict()#key:reviewid  value:votes count(cool) 

for bizID in bizURL:
    url=bizURL[bizID]

    #get the List of yelp urls to scrape
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)


    #get reviewID and userID
    review=soup.find('div',itemprop="review")
    reviews=soup.findAll('div',{"itemprop":"review"})
    for div in reviews:
        reviewBiz[div["data-review-id"]]=bizID
        reviewUser[div["data-review-id"]]=div["data-signup-object"]
    

        #get rating and votes
        reviewStar[div["data-review-id"]]=div.find('meta',itemprop="ratingValue")["content"]
        useful=div.find('a',{"rel":"useful"}).find('span',{"class":"count"})
        reviewUseful[div["data-review-id"]]=useful.text
        funny=div.find('a',{"rel":"funny"}).find('span',{"class":"count"})
        reviewFunny[div["data-review-id"]]=funny.text
        cool=div.find('a',{"rel":"cool"}).find('span',{"class":"count"})
        reviewCool[div["data-review-id"]]=cool.text

#Store review information into csv file
directoryForDB = "/Users/jessicazhao/Documents/homework/CC/"
if not os.path.exists(directoryForDB):
	os.makedirs(directoryForDB)
with open(directoryForDB+"review.csv","w") as csvfile:
    fieldnames=["reviewID","bizID","userID","rating","userful","funny","cool"]
    writer=csv.DictWriter(csvfile,fieldnames)
    
    writer.writeheader()
    for key in reviewBiz:
        writer.writerow({"reviewID":key,"bizID":reviewBiz[key],"userID":reviewUser[key],"rating":reviewStar[key],"userful":reviewUseful[key],"funny":reviewFunny[key],"cool":reviewCool[key]})
