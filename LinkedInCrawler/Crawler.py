from win32com.client import Dispatch
import time
from random import randrange
import Scraper
import DB

print "Current Time is: " + str(time.strftime("%Y-%m-%d %H:%M"))


#TEST


ie = Dispatch("InternetExplorer.Application")  #Create browser instance.
ie.Visible = 1      # Make it visible (0 = invisible)
ie.Navigate("http://www.linkedin.com")
print "Waiting for log in."
time.sleep(60)


URL = "http://www.linkedin.com/profile/view?id="
count = 0
maxcount = 240 + randrange(120)


while(count<maxcount):
    count = count +1
    try:
        LNid = DB.nexttovisit()
        #Mark as visited
        DB.visit(LNid,3)
        
        print "Downloading:" + str(LNid)
        out = open("C:\\Users\\J\\Documents\\Projects\\AMN\\LinkedCrawler\\Output\\" + str(LNid) + ".html",'w')
        ie.Navigate(URL + str(LNid))
        
        #Random Sleep
        sleeptime = 120 + randrange(60)
        print "Sleeping for " + str(sleeptime) + " seconds"
        time.sleep(sleeptime)

        text = ie.Document.body.innerHTML
        #text is in unicode, so get it into a string
        text = unicode(text)
        text = text.encode('ascii','ignore')
        out.write(text)
        out.close()
        Scraper.scraper(text)

        #Scrape Connecton distance and update
        Connection = 3
        if(text.count('is your connection" class="degree-icon ">1<sup>st</sup></abbr></span><div id="badge-container" data-li-template="badge"><div class="editable-item" id="badge"></div></div></div><div data-li-template="p2_basic_info">')==1):
            Connection = 1
        DB.visit(LNid,Connection)
        
        #Check to see if we have been blocked
        if text.count('LinkedIn is Momentarily Unavailable')>0:
            print "We've been blocked - Holding for 24 hours"
            time.sleep(60*60*24)
    except:
        ie.Quit()
        ie = Dispatch("InternetExplorer.Application")  #Create browser instance.
        ie.Visible = 1      # Make it visible (0 = invisible)
        ie.Navigate("http://www.linkedin.com")
        #try:
        #    print "Failed:" + str(LNid)
        #except:
        #    print "Crawler failed so bad it can't even figure out where"
        #time.sleep(600)
        #print "ERROR"
