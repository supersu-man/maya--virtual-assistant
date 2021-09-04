import requests
from credentials import glearn, moodle
from bs4 import BeautifulSoup
import datetime

s = requests.session()

def soupify(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup

def glearnFormData(htmlsource):
    soup = soupify(htmlsource)
    viewstate = soup.find(id="__VIEWSTATE")['value']
    viewstategenerator = soup.find(id="__VIEWSTATEGENERATOR")['value']
    eventvalidation = soup.find(id="__EVENTVALIDATION")['value']
    requestBody = {
        "__VIEWSTATE": viewstate,
        "__VIEWSTATEGENERATOR": viewstategenerator,
        "__EVENTVALIDATION": eventvalidation,
        "txtusername": glearn['username'],
        "password": glearn['password'],
        "Submit": "Login"
    }
    return requestBody

def moodleFormData(htmlsource):
    soup = soupify(htmlsource)
    logintoken = soup.find("input", {"name": "logintoken"})['value']
    requestBody = {
        "logintoken": logintoken,
        "username": moodle['username'],
        "password": moodle['password']
    }
    return requestBody

def isWrongCredentials(text):
    return "Invalid" in text

def isWrongCredentials2(text):
    return "Invalid login" in text

def isGlearnLoggedIn():
    response1 = requests.get("https://gstudent.gitam.edu/Welcome.aspx").text
    response2 = s.get("https://gstudent.gitam.edu/Welcome.aspx").text
    return not soupify(response1).find('title').text == soupify(response2).find('title').text

def isMoodleLoggedIn():
    response1 = requests.get("https://learn.gitam.edu/calendar/view.php?view=upcoming")
    response2 = s.get("https://learn.gitam.edu/calendar/view.php?view=upcoming")
    return not soupify(response1.text).find('title').text == soupify(response2.text).find('title').text

def loginGlearn():
    source = s.get("https://login.gitam.edu/Login.aspx").text
    response = s.post("https://login.gitam.edu/Login.aspx", glearnFormData(source))
    if isWrongCredentials(response.text):
        print("Wrong Credentials")

def loginMoodle():
    response1 = s.get("https://learn.gitam.edu/login/index.php")
    response2 = s.post("https://learn.gitam.edu/login/index.php", moodleFormData(response1.text))
    if isWrongCredentials2(response2.text):
        print("Wrong Credentials.")

def logoutMoodle():
    response = s.get("https://learn.gitam.edu/calendar/view.php?view=upcoming")
    soup = soupify(response.text)
    logoutLink = soup.find('a', {'aria-labelledby': 'actionmenuaction-6'})['href']
    s.get(logoutLink)

def getAttendance():
    if not isGlearnLoggedIn():
        loginGlearn()
    attendanceResponseText = s.get("https://gstudent.gitam.edu/Attendance_new.aspx").text
    attendance = soupify(attendanceResponseText).find(id="MainContent_lbltotal").text
    return attendance

def getTimetable():
    if not isGlearnLoggedIn():
        loginGlearn()
    response = s.get("https://gstudent.gitam.edu/Newtimetable.aspx").text
    response1 = s.get("https://gstudent.gitam.edu/G-Learn.aspx").text
    v = soupify(response).find(id='MainContent_grd1')
    x = soupify(response1).find(id='ContentPlaceHolder1_GridView2')
    timings = []
    classes = []
    subjectCodes = []
    for i in x.findAll('td'):
        subjectCodes.append((i.find('h4').text, i.find('h6').text))
    for i in v.findAll('tr'):
        if 'th' in str(i):
            for j in i.findAll('th'):
                timings.append(j.text)
        if 'td' in str(i):
            eachDay = []
            for j in i.findAll('td'):
                y = j.text
                for k in subjectCodes:
                    if k[0] in j.text:
                        y = k[1]
                        break
                eachDay.append(y)
            classes.append(eachDay)
    return timings, classes

def getTimetableToday():
    weekday,classes = getTimetable()
    now = datetime.datetime.now()
    if now.weekday()>4:
        return None
    lst = []
    nextclass = ()
    for i in range(len(weekday)):
        if classes[now.weekday()][i] != '':
            lst.append((convertTo12Hour(weekday[i]), classes[now.weekday()][i]))
            if not weekday[i] == 'WEEKDAY':
                hour = int(weekday[i].split("to")[0].split(':')[0])
                if len(weekday)>1 and now.hour < hour and nextclass==():
                    nextclass = convertTo12Hour(weekday[1]), classes[now.weekday()][0]
                elif hour==now.hour and now.minute<15:
                    nextclass = convertTo12Hour(weekday[i]), classes[now.weekday()][i]
                elif hour==now.hour and now.minute>=15 and i+1<len(weekday):
                    nextclass = convertTo12Hour(weekday[i+1]), classes[now.weekday()][i+1]

    return nextclass,lst[1:]

def convertTo12Hour(text):
    try:
        hour = int(text.split("to")[0].split(':')[0])
        if hour > 12:
            hour = hour - 12
        x = text
        x = "{}:{} to {}:{}".format(hour, x.split('to')[0].split(':')[1], hour, x.split('to')[1].split(':')[1])
        return x
    except:
        return text

def getUpcomingActivities():
    if not isMoodleLoggedIn():
        loginMoodle()
    response = s.get("https://learn.gitam.edu/calendar/view.php?view=upcoming")
    tup = []
    soup = soupify(response.text)
    for i in soup.findAll('div', {'class': 'event m-t-1'}):
        activity = i.find('h3', {'class': 'name d-inline-block'}).text
        time = i.find('div', {'class': 'col-11'}).text
        link=''
        try:
            link = i.find('div', {'class': 'description-content col-11'}).find('a')['href']
        except:
            pass
        tup.append((activity, time, link))
    logoutMoodle()
    return tup

