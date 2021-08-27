from speech import listen, say

from browser_commands import googleSearch, openWebsite, whatIs
from gitam_fetch import getTimetable, getTimetableToday, getAttendance, getUpcomingActivities
import threading


def actions(intent1,intent_value1):
    if intent1 == 'openBrowser':
        thread = threading.Thread(target=say, args=("Opening " + intent_value1,), daemon=True)
        thread.start()
        url = googleSearch(intent_value1)
        openWebsite(url)
    if intent1 == 'defineWord':
        summary = whatIs(intent_value1)
        print(summary)
        say(summary)
    if intent1 == 'timetable':
        print(getTimetable())
    if intent1 == 'upcomingClasses':
        val = getTimetableToday()
        say("You got {} classes today".format(len(val[1])))
        if len(val[0])==2:
            say("Your next class is {} at {}".format(val[0][1],val[0][0]))
        else:
            say("You are done with classes")
        print(val)





