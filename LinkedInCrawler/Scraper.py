import shutil
import string
import os
import socket
import urllib2
import re
import sets
import time
import threading
import DB

# Setup Regex
reID = re.compile('\\<a\\ title\\=\\"View.*?\\<\\/p\\>\\<\\/li\\>',re.DOTALL)
reURL = re.compile('www.linkedin.com.profile.view.id=\d{4,12}',re.DOTALL)

HighTitles = [' ceo', 'ceo ', 'cio ',' cio','coo ',' coo','cto ',' cto ',' cfo','cfo ','cpo ',' cpo','vp','chief executive officer','chief information officer','chief technology officer','chief financial officer','chief operations officer',' vp ',' evp ','president','director','board']
MedTitles =  ['manager','recruiter','talent','product manager']
NegIndicators = ['creative director','art director','business development','sunlife','account manager','animation','account','artist']

def scraper(Data):
    #try:
        ID = re.findall(reID,Data)
        while len(ID)>0:
            item = ID.pop()
            score = 0
            if(item.count("ghosts")==0):
                    score = score + 1
            #Basic brute force clean up
            item = item.split('<h4><a href="').pop()
            item = item.replace('</a></h4><p class="browse-map-title">','|')
            item = item.replace('</p></li>','')
            item = item.replace('">','|')
            item = item.replace('http://www.linkedin.com/profile/view?id=','')
            item = item.replace('https://www.linkedin.com/profile/view?id=','')
            item = item.split('|')
            name = item[1].replace("'","")
            title = item[2].replace("'","")
            LNid = item[0].split('&').pop(0)
            item = name + '|' + title + '|' + LNid

            #Get the Score
            title = title.lower()
            
            #Start by looking for key job titles
            for Title in HighTitles:
                if (" " + title +  " ").count(" " + Title + " ")>0:
                    score = score + 2         
            for Title in MedTitles:
                if (" " + title + " ").count(" " + Title + " ")>0:
                    score = score + 1
                    
            #Then add points for location
            locationscore = 0
            if (Data.lower().count('vancouver'))>0:
                locationscore = locationscore + 2
            if (Data.lower().count('canada'))>0:
                locationscore = locationscore + 1
            if (Data.lower().count('port moody'))>0:
                locationscore = locationscore + 1
            if (Data.lower().count('coquitlam'))>0:
                locationscore = locationscore + 1
            if (Data.lower().count('new westminster'))>0:
                locationscore = locationscore + 1
            if (Data.lower().count('richmond'))>0:
                locationscore = locationscore + 1
            if (Data.lower().count('white rock'))>0:
                locationscore = locationscore + 1
            if (Data.lower().count('surrey'))>0:
                locationscore = locationscore + 1
            if (locationscore>3):
                locationscore = 3
                
            score = score + locationscore
            #Add points for high connection count of source
            if (Data.lower().count('500+'))>0:
                score = score + 1

            #Subtract points for negitive indicators
            if (Data.lower().count('sales'))>3:
                score = score - 1
            for Title in NegIndicators:
                if (" " + title +  " ").count(" " + Title + " ")>0:
                    score = 0      
            if score<0:
                score = 0
                             
            #test to see if this record has been seen before
            if DB.test(LNid) == True:
                DB.update(LNid, name, title, score)
                print "Updating Record: " + LNid + " Score: " + str(score)
            if DB.test(LNid) == False:
                DB.add(LNid, name, title, score, 3) #Assume a connection distance of 3 until we actually visit the profile
                print "Adding Record: " + LNid + " Score: " + str(score)
        print
    #except:
    #    print "Error: Scrapper - " + str(LNid)

def viewscraper(Data):
    try:
        Data = Data.split("viewers-container")
        Data = Data.pop(1)
        InList = open('C:\\Users\\J\\Documents\\Projects\\AMN\\LinkedCrawler\\VisitLog.txt','r')
        IDList = re.findall(reURL,Data)
        for ID in IDList:
            ID = ID.replace('www.linkedin.com/profile/view?id=','')
            if (DB.testvisitor(ID)==False):
                DB.addvisitor(ID)
                print "New visitor logged: " + str(ID)
    except:
        print "Error: Vistor Log" 

