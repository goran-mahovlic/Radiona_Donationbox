import sqlite3
import MySQLdb
from os import sys

DonationBox_Name="D11111"
mySqlServer = ""
mySqlServerDatabase = ""
mySqlServerUser = ""
mySqlServerPassword = ""

def getMoneyForProject_local(money_project):
    if sys.platform == 'win32' and sys.getwindowsversion()[0] >= 5:
        print ("No log on windows")
    elif sys.platform == 'linux2':
        conn = sqlite3.connect("/home/donationbox/donationboxDatabase.sqlite",detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        cursor.execute("SELECT sum(inserted) FROM (SELECT id,inserted,project FROM money WHERE project = ('" + str(money_project) + "'))")
        money_in_project = cursor.fetchone()
        conn.close
#        print "For project:" + str(money_project) + " we have collected:" + str(money_in_project).strip( ')(,' ) + "kn"
    return str(money_in_project).strip( ')(,' )
	
def getMoneyForProject_remote(remote_project):
    # Open database connection
    db = MySQLdb.connect(mySqlServer,mySqlServeruser,mySqlServerPassword,mySqlServerDatabase)
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    today = str(today)
    sql = ("SELECT money FROM donationbox.moneyToProject WHERE project = %s" %  ("'" + remote_project + "'"))
    # Execute the SQL command
    cursor.execute(sql)
    results = cursor.fetchone()
#    print results
    return results

def setMoneyForProject_remote(remote_money,remote_project):
#    print ("UPDATE `donationbox`.`moneyToProject` SET `money` = %s WHERE `moneyToProject`.`project` = %s;" % (remote_money,remote_project)) 
    # Open database connection
    db = MySQLdb.connect(mySqlServer,mySqlServeruser,mySqlServerPassword,mySqlServerDatabase)
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
#    sql = ("UPDATE `donationbox`.`moneyToProject` SET `money`=%s WHERE `project`=%s)" % (remote_money,remote_project)
    sql = ("UPDATE `donationbox`.`moneyToProject` SET `money` = %s WHERE `moneyToProject`.`project` = %s;" % (remote_money,remote_project)) 

    try:
    # Execute the SQL command
       cursor.execute(sql)
       # Commit your changes in the database
       db.commit()
    except:
       # Rollback in case there is any error
        db.rollback()
       # Disconnect from server
    db.close()

def checkAndUpdate():
    for i in range(0, 5):
#        print "Updating project: %s" % (i)
#        print "Setting money to: %s" % (getMoneyForProject_local(i))
        setMoneyForProject_remote(getMoneyForProject_local(i),i)
	
checkAndUpdate()
