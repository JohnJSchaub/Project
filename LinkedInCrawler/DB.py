import MySQLdb
import time
from datetime import date, timedelta

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="MySQLPassword", # your password
                      db="crawler") # name of the data base


def test(LNid):
    cur = db.cursor() 

    # Use all the SQL you like
    cur.execute("SELECT count(*) FROM Linkedin_Crawler where id = " + str(LNid))
    # print all the first cell of all the rows
    for row in cur.fetchall():
        if row[0]==0:
            result = False
        else:
            result = True
    return result

def add(LNid, Name, Title, Score,Connection):
    cur = db.cursor()
    query = "INSERT INTO LinkedIn_Crawler VALUES (" + str(LNid) + ",'" + Name + "','" + Title + "'," + str(Score) + ",False,'" + str(time.strftime("%Y-%m-%d %H:%M")) + "',0,0,0," + str(Connection)+ ")"
    cur.execute(query)
    db.commit()

def visit(LNid, Connection):
    cur = db.cursor()
    query = "UPDATE LinkedIn_Crawler SET Visited=True, ViewedDate = '" + str(time.strftime("%Y-%m-%d %H:%M")) + "', Connection_Dist =" + str(Connection) + " WHERE id=" + str(LNid)
    cur.execute(query)
    db.commit()
      

def update(LNid, Name, Title, Score):
    cur = db.cursor()
    cur.execute("SELECT LinkCount FROM Linkedin_Crawler where id = " + str(LNid))
    try:
        if CrawlName == "J":
            CurrentCount = int(cur.fetchone()[0]) + 1
        else:
            CurrentCount = int(cur.fetchone()[0])
    except:
        CurrentCount = 1
    cur = db.cursor()  
    query = "UPDATE LinkedIn_Crawler SET Name='" + Name + "', Company = '" + Title + "', Score = '" + str(Score) + "', LinkCount = " + str(CurrentCount) + " WHERE id=" + str(LNid)
    cur.execute(query)
    db.commit()

def nexttovisit():
    cur = db.cursor()
    query = "select max(LinkCount) from linkedin_crawler where visited = false"
    cur.execute(query)
    MaxLinkCount = int(cur.fetchone()[0])

    if MaxLinkCount > 4:
        cur = db.cursor()
        query = "select id from linkedin_crawler where LinkCount = (select max(LinkCount) from linkedin_crawler where visited = false) and visited = false"
        cur.execute(query)
        return int(cur.fetchone()[0])

    else:
        cur = db.cursor()
        query = "select id from linkedin_crawler where Score = (select max(Score) from linkedin_crawler where visited = false) and  LinkCount = (select max(LinkCount) from linkedin_crawler where visited = false and Score = (select max(Score) from linkedin_crawler where visited = false)) and visited = false"
        cur.execute(query)
        return int(cur.fetchone()[0])

def testvisitor(LNid):
    #Look for your own id if so ignore it.
    if LNid == '10509459':
        return True    
    cur = db.cursor()
    yesterday = date.today() - timedelta(1)
    query = "select count(*) from visitor_log where id = " + str(LNid) + " and VisitedDate > '" + str(yesterday.strftime("%Y-%m-%d")) + "'"
    #print query
    cur.execute(query)
    if int(cur.fetchone()[0])==0:   
        return False
    else:
        return True
                                                                                                        
def addvisitor(LNid):
    cur = db.cursor()
    query = "INSERT INTO Visitor_Log VALUES (" + str(LNid) + ",'" + str(time.strftime("%Y-%m-%d")) + "')"
    #print query
    cur.execute(query)
    db.commit()
