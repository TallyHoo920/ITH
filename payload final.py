# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        weekends-r-mine
# Purpose: To update rota if there are any empty shifts on weekends. 
# Run time: 2.5s
# Author:      ahmedt
# Created:     05/10/2018
# Copyright:   (c) ahmedt 2018
#-------------------------------------------------------------------------------
import requests
import re
import time
import imaplib
import email

weekNumber = 66
day = ['Saturday', 'Saturday', 'Sunday', 'Sunday']
date = ['2018-11-03', '2018-11-04']
ORG_EMAIL   = "@port.ac.uk"
FROM_EMAIL  = "talhaa.ahmed" + ORG_EMAIL
FROM_PWD    = 'ednqrcgmjbffqrdj'
SMTP_SERVER = "pop.gmail.com"
SMTP_PORT   = 995

def read_email_from_gmail():
    starttime = time.time()
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL,FROM_PWD)
    success = False
    while success == False:
        mail.select('inbox')
        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()   
        #first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        typ, data = mail.fetch(str(latest_email_id), '(RFC822)' )
        
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_subject = msg['subject']
                email_to = msg['to']
                email_from = msg['from']
                if 'natalie.wragg@port.ac.uk' in email_from and 'ith-shifts-group@port.ac.uk' in email_to and '[ITH Shifts]' in email_subject:
                    print('From : ' + email_from + '\n')
                    print('To: ' + email_to + '\n')
                    print('Subject : ' + email_subject + '\n')
                    success = True
                else:
                    print('Fail')
                    success = False
    
            endtime = time.time()
        print('Time taken: {}s'.format(endtime - starttime))
    return success
    #except Exception as e:
    #    print(str(e))
        
def stuff(data):
    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            print(msg)        
            email_subject = msg['subject']
            print(email_subject)

def getRefValue(i):
    if i % 2 == 0:
        ref = 1
    else:
        ref = 2
    return ref
        
def getUrlData(weekNumber, templateNumber, ref, day):
    url = 'https://ith.port.ac.uk/public/app/rota-rebuild/php/shared.php?action=getdayShiftInfo&week={}&template={}&shiftLocation=ul{}&shiftDay={}'.format(weekNumber, templateNumber, ref, day)
    urlRequest = requests.get(url)
    urlText = str(urlRequest.text)
    urlString = urlText.replace('\\', '')
    urlData = urlString.replace('"', '')
    return urlData

def fixList(theList, replacement='data-user='):
    for i in range(len(theList)):
        theList[i] = theList[i].replace(replacement, '')
    return theList

def removeDuplicates(listofElements):
    # Create an empty list to store unique elements
    uniqueList = []

    # Iterate over the original list and for each element
    # add it to uniqueList, if its not already there.
    for elem in listofElements:
        if elem not in uniqueList:
            uniqueList.append(elem)

    # Return the list of unique elements
    return uniqueList

def findAndFix(find, info):
    initialData = re.findall(find, info)
    if find == 'data-row=.....':    
        fixedData0 = fixList(initialData, 'data-row=')
        fixedData = removeDuplicates(fixedData0)
    else:
        fixedData = fixList(initialData)
    return fixedData

def dashChecker(someList):
    #This is supposed to check for a dash to see which shift is empty, 
    #however due to use of reg-edit, the text format is messed up. 
    #so we search for ' da' instead.
    if ' da' in someList:
        return True
    else:
        return False

def indexNumber(myList):
    for i, elem in enumerate(myList):
        if ' da' in elem:
           return i

def sendPayload(day, dayRowList, date, weekNumber, dayString, offSwitch=True):
    if offSwitch:
        print('Force offswitch is turned on. No rota can be updated.')
        return False
    
    index = indexNumber(day)
    payload = 'https://ith.port.ac.uk/public/app/rota-rebuild/php/shared.php?action=swapShift&row={}&ad=TIA&userID=103&date={}&weekID={}'
    requests.get(payload.format(dayRowList[index], date, weekNumber))
    print('Sent request to {}'.format(dayString))
    return True

def main():
    start = time.time()
    #read_email_from_gmail()
        
    for j in range(1,3):
        for i in range(4):
            ref = getRefValue(i)                
            urlData = getUrlData(weekNumber, j, ref, day[i])
            
            if i == 0:
                sat0 = findAndFix('data-user=...', urlData)
                sat0row = findAndFix('data-row=.....', urlData)
            elif i == 1:
                sat1 = findAndFix('data-user=...', urlData)
                sat1row = findAndFix('data-row=.....', urlData)
            elif i == 2:
                sun0 = findAndFix('data-user=...', urlData)
                sun0row = findAndFix('data-row=.....', urlData)
            else:
                sun1 = findAndFix('data-user=...', urlData)
                sun1row = findAndFix('data-row=.....', urlData)
                
        if dashChecker(sat0):
            success = sendPayload(sat0, sat0row, date[0], weekNumber, 'SAT0')
            
        elif dashChecker(sat1):
            success = sendPayload(sat1, sat1row, date[0], weekNumber, 'SAT1')
            
        elif dashChecker(sun0):
            success = sendPayload(sun0, sun0row, date[1], weekNumber, 'SUN0')
            
        elif dashChecker(sun1):
            success = sendPayload(sun0, sun1row, date[1], weekNumber, 'SUN1')
            
        else:
            print('No date changed for template {}'.format(j))
            success = False

        print(sat0, sat1, sun0, sun1)
        print(sat0row, sat1row, sun0row, sun1row)
    end = time.time()
    print(end - start)
    return success

if __name__ == '__main__':
    main()

