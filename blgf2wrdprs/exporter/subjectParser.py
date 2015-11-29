__author__ = 'smirzai'

from HTMLParser import HTMLParser
import urllib2



class PostsCategoryParser(HTMLParser):
    isInPost = False


    def getPostsInCategoty(self, result, base, url):



        self.nextPage = ""
        self.hasNextPage  = True
        while self.hasNextPage:
            self.hasNextPage = False
            data = urllib2.urlopen(base + url + ("" if self.nextPage == "" else "?p=" + self.nextPage ))
            content = data.read().decode('utf-8')
       #     result[url[5:-5]] = []
            self.result = result
            self.url = url
            self.isInH1 = False

            self.feed(content)

    def handle_starttag(self, tag, attrs):

        if tag == "h2" and len(attrs) > 0 and len(attrs[0]) > 1 and attrs[0][0] == "class" and attrs[0][1] == "hl":
            self.isInH1 = True;
            return

        if not self.isInH1 and tag == "a" and len(attrs) > 0 and len(attrs[0]) > 1 and attrs[0][0] == "href" and attrs[0][1].startswith('?'):
            np = attrs[0][1][3:]
            try:
                np = int(np)
            except:
                return
            if self.nextPage == "" or np > int(self.nextPage):
                self.nextPage = str(np)
                self.hasNextPage = True

        if self.isInH1  and  tag == "a" and len(attrs) > 0 and len(attrs[0]) > 0 and attrs[0][0] == "href" and attrs[0][1].startswith("/post"):
            postNumber = attrs[0][1][6:-5]
            subjectNumber = self.url[5:-5]
            if postNumber in self.result:

                self.result[postNumber] += [subjectNumber]
            else:
                self.result[postNumber] = [subjectNumber]
            return



    def handle_endtag(self, tag):
        if self.isInH1 and tag == "h2":
            self.isInH1 = False
            return







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

        if tag == "div" and len(attrs) > 0 and len(attrs[0]) > 1 and attrs[0][0] == "class" and attrs[0][1] == "Sidebar":
            self.inSideBar = False

        if tag == "a" and len(attrs) > 0 and len(attrs[0]) > 0 and attrs[0][0] == "href" and attrs[0][1].startswith("/cat-"):
            self.last_subject = attrs[0][1]
            self.postsCategoryParser.getPostsInCategoty(self.result, self.url , attrs[0][1])
            self.inSubjects = True

    def handle_endtag(self, tag):
        if self.inSubjects and tag == "a":
            self.inSubjects = False

    def handle_data(self, data):
        if self.inSubjects:
            self.subjects[self.last_subject[5:-5]] = data

