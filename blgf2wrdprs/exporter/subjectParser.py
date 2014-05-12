__author__ = 'smirzai'

from HTMLParser import HTMLParser
import urllib2



class PostsCategoryParser(HTMLParser):
    isInPost = False


    def getPostsInCategoty(self, result, base, url):

        data = urllib2.urlopen(base + url)
        content = data.read().decode('utf-8')
        result[url] = []
        self.result = result
        self.url = url

        self.feed(content)

    def handle_starttag(self, tag, attrs):
        if tag == "div" and attrs[0][0] == "class" and attrs[0][1] == "posttitle":
            self.isInPost = True
        if tag == "a" and attrs[0][0] == "href" and attrs[0][1].startswith("/post/"):
            if attrs[0][1] in self.result:
                self.result[attrs[0][1]] += [self.url]
            else:
                self.result[attrs[0][1]] = [self.url]


    def handle_endtag(self, tag):
        if tag == "div":
            self.isInPost = False





class SubjectListParser(HTMLParser):
    test = 0
    inSidebar = False
    inSubjects = False
    postsCategoryParser = PostsCategoryParser()
    result = dict()
    subjects = dict()
    last_subject = ""

    def parsePage(self, urll):
        self.url = urll
        data = urllib2.urlopen(urll)

        content = data.read().decode('utf-8')
        self.result = dict()
        self.feed(content)
        return (self.subjects, self.result)

    def handle_starttag(self, tag, attrs):
        if tag == "div" and attrs[0][0] == "class" and attrs[0][1] == "Sidebar":
            self.inSideBar = False
        if tag == "a" and attrs[0][0] == "href" and attrs[0][1].startswith("/category/"):
            self.last_subject = attrs[0][1]
            self.postsCategoryParser.getPostsInCategoty(self.result, self.url , attrs[0][1])
            self.inSubjects = True

    def handle_endtag(self, tag):
        if self.inSubjects and tag == "a":
            self.inSubjects = False

    def handle_data(self, data):
        if self.inSubjects:
            self.subjects[self.last_subject] = data
            print self.last_subject, "-->", data
