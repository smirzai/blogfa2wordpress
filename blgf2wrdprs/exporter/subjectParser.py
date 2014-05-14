__author__ = 'smirzai'

from HTMLParser import HTMLParser
import urllib2



class PostsCategoryParser(HTMLParser):
    isInPost = False


    def getPostsInCategoty(self, result, base, url):

        data = urllib2.urlopen(base + url)
        content = data.read().decode('utf-8')
   #     result[url[5:-5]] = []
        self.result = result
        self.url = url

        self.feed(content)

    def handle_starttag(self, tag, attrs):
        if tag == "div" and attrs[0][0] == "class" and attrs[0][1] == "bodyposts":
            self.isInPost = True
        if self.isInPost  and  tag == "a" and attrs[0][0] == "href" and attrs[0][1].startswith("/post"):
            postNumber = attrs[0][1][6:-5]
            subjectNumber = self.url[5:-5]
            if postNumber in self.result:

                self.result[postNumber] += [subjectNumber]
            else:
                self.result[postNumber] = [subjectNumber]


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
        if tag == "a" and attrs[0][0] == "href" and attrs[0][1].startswith("/cat-"):
            self.last_subject = attrs[0][1]
            self.postsCategoryParser.getPostsInCategoty(self.result, self.url , attrs[0][1])
            self.inSubjects = True

    def handle_endtag(self, tag):
        if self.inSubjects and tag == "a":
            self.inSubjects = False

    def handle_data(self, data):
        if self.inSubjects:
            self.subjects[self.last_subject[5:-5]] = data

