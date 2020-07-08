import requests
import time
from datetime import datetime
import hashlib
import smtplib, ssl
from getpass import getpass

class NTUepoWatcher():
    loginURL = 'https://if163.aca.ntu.edu.tw/eportfolio/login.asp'
    toPostURL = 'https://web2.cc.ntu.edu.tw/p/s/login2/p1.php'
    gradePageURL = 'https://if163.aca.ntu.edu.tw/eportfolio/student/CourseSem.asp'
    session = requests.session()
    
    def __init__(self, epoUserName, epoPassword, senderEmail, senderPassword, receiverEmail, timeInterval):
        self.epoUserName = epoUserName
        self.epoPassword = epoPassword
        self.senderEmail = senderEmail
        self.senderPassword = senderPassword
        self.receiverEmail = receiverEmail
        self.timeInterval = timeInterval
        
    def createLoginPayload(self):
        return {'user':self.epoUserName, 'pass':self.epoPassword}
        
    def makeMessage(self, oldContent, newContent):
        message = """\
        Subject: Something has changed!

        Something has changed on NTU e-portfolio! Check it out."""
        return message
        
        
    def sendEmail(self, message):
        context = ssl.create_default_context()
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(self.senderEmail, self.senderPassword)
            server.sendmail(self.senderEmail, self.receiverEmail, message)
            
    def login(self):
        self.session.get(self.loginURL)
        self.session.post(self.toPostURL, self.createLoginPayload())
        
    def getGradePage(self):
        return self.session.get(self.gradePageURL)
        
    def getTime(self):
        return "[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "]"
    
    def run(self):
        print(self.getTime() + " start watching...")
        self.login()
        oldContent = self.getGradePage().content
        while True:
            try:
                time.sleep(self.timeInterval)
                newContent = self.getGradePage().content
                if oldContent == newContent:
                    print(self.getTime() + " nothing changed...")
                    oldContent = newContent
                else:
                    print(self.getTime() + " something has changed!")
                    self.sendEmail(self.makeMessage(oldContent, newContent))
                    oldContent = newContent
            except (EOFError, KeyboardInterrupt):
                print('Keyboard Interrupt\n')
                break
            except Exception as e:
                print(e)
                break
                    
def main():
    epoUserName = 'bxxxxxxxx'
    epoPassword = getpass('NTU e-portfolio password: ')
    senderEmail = 'yyy@gmail.com'
    senderPassword = getpass('Gmail password: ')
    receiverEmail = 'zzz@gmail.com'
    timeInterval = 10
    watcher = NTUepoWatcher(epoUserName, epoPassword, senderEmail, senderPassword, receiverEmail, timeInterval)
    watcher.run()
    
if __name__ == '__main__':
    main()
