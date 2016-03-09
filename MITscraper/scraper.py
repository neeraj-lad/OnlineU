import sys
import urllib2
from lxml import html, etree
import re

URL = "http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-042j-mathematics-for-computer-science-fall-2010/index.htm"

class Course():
    def __init__(self, title, description, url, instructors, cal, assignments, lec):
        self.title = title
        self.description = description
        self.url = url
        self.instructors = instructors
        self.calendar = cal
        self.assignments = assignments
        self.lectures = lec

    def __repr__(self):
        # Title
        s = "Title: " + self.title + "\n"
        # Course URL
        s = s + "URL: " + self.url + "\n"
        # Instructors
        s = s + "Instructor(s):\n"
        for instructor in self.instructors:
            s = s + instructor + "\n"
        # Calendar
        s = s + "Calendar:\n"
        for entry in self.calendar:
            for part in entry:
                try:
                    s = s + str(part) + "   "
                except UnicodeEncodeError:
                    continue
            s = s + "\n"
        # Lectures
        s = s + "Lectures:\n"
        for lecture in self.lectures:
            s = s + lecture[0] + "\n"
        # Assignments
        s = s + "Assignments:\n"
        for a in self.assignments:
            s = s + str(a[2]) + "\n"
        return s

    def getSchedule():
        pass

def calendar(url):
    return url.replace("/index.htm", "/calendar")

def assignments(url):
    return url.replace("/index.htm", "/assignments")

def lectures(url):
    return re.sub("/index.*", "/video-lectures", url)

def lectures2(url):
    return re.sub("/index.*", "/lecture-videos", url)

def loadPage(url):
    #print "Loading " + url
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    return response.read()

def main(args):
    if len(args) > 0:
        URL = args[0]

    # Load the main coursepage
    page = loadPage(URL)

    # Parse the webpage
    #print "Scraping page"
    tree = html.fromstring(page)
    title = tree.xpath('//h1/text()')[0]

    instructors = tree.xpath('//p[@class="ins"]/text()')
    description = tree.xpath('//div[@id="description"]/div/p/text()')[0]

    # Load calendar
    page = loadPage(calendar(URL))
    tree = html.fromstring(page)
    rows = tree.xpath('//tr')

    # Parse calendar
    cal = []
    for row in rows:
        crow = []
        for element in row:
            crow.append(element.text)
        try:
            crow[0] = int(crow[0])
        except TypeError:
            continue
        except ValueError:
            continue
        cal.append(crow)

    # Load assignments
    page = loadPage(assignments(URL))
    tree = html.fromstring(page)
    rows = tree.xpath('//tr')

    # Parse assignments
    c = []
    for row in rows:
        crow = []
        for element in row:
            crow.append(element.text)
            for sub in element:
                if sub.tag == "a":
                    crow.append(sub.attrib['href'])
        try:
            crow[0] = int(crow[0])
        except TypeError:
            continue
        except ValueError:
            continue
        c.append(crow)

    # Load lectures
    try:
        page = loadPage(lectures(URL))
    except urllib2.HTTPError:
        try:
            page = loadPage(lectures2(URL))
        except urllib2.HTTPError:
            print "Could not load: " + lectures(URL)
            sys.exit()
    tree = html.fromstring(page)
    ls = tree.xpath('//div[@class="medialisting"]')

    # Parse lectures
    result = []
    for lecture in ls:
        link = lecture[0].attrib['href']
        t = lecture[0].attrib['title']
        if link.startswith("/"):
            result.append([t, "http://ocw.mit.edu" + link])
        else:
            result.append([t, link])

    # Compile everything together
    course = Course(title, description, URL, instructors, cal, c, result)
    return course


if __name__ == "__main__":
    main(sys.argv[1:])