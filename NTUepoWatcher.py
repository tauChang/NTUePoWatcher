import requests
from bs4 import BeautifulSoup
import time
import hashlib
import smtplib, ssl

epoUserName = 'xxx'
epoPassword = 'yyy'
senderEmail = 'zzz@gmail.com'
senderPassword = 'vvv'
receiverEmail = senderEmail
timeInterval = 10


payload = {'user':epoUserName, 'pass':epoPassword}
loginURL = 'https://if163.aca.ntu.edu.tw/eportfolio/login.asp'
toPostURL = 'https://web2.cc.ntu.edu.tw/p/s/login2/p1.php'
gradeSectionURL = 'https://if163.aca.ntu.edu.tw/eportfolio/student/CourseSem.asp'

port = 587  # For starttls
smtpServer = 'smtp.gmail.com'
message = """\
Subject: Something has changed!

Something has changed on NTUepo! Check it out."""


# create session
session= requests.session()

# access log in page to obtain cookie
session.get(loginURL)

# log in with username and password
session.post(toPostURL, payload)

# access the grade page and hash
response = session.get(gradeSectionURL)
oldHash = hashlib.sha224(response.content).hexdigest()


while True:
    try:
        time.sleep(10)
        response = session.get(gradeSectionURL)
        newHash = hashlib.sha224(response.content).hexdigest()
        if newHash == oldHash:
            print('nothing changed...')
            oldHash = newHash
            continue
        else:
            print('DAMN SOMETHING CHANGED!! BRO')
            break
            context = ssl.create_default_context()
            with smtplib.SMTP(smtpServer, port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(senderEmail, senderPassword)
                server.sendmail(senderEmail, receiverEmail, message)
            oldHash = newHash
    except (EOFError, KeyboardInterrupt):
        print('ctrl c pressed')
        break
    except:
        print('fuck something wrong')
        break
    


#soup = BeautifulSoup(result.content.decode('Big5'), 'html.parser')
#print(soup.prettify())


