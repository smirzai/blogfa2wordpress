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
            
            self.result[self.url] += attrs[0][1]


    def handle_endtag(self, tag):
        if tag == "div":
            self.isInPost = False





class SubjectListParser(HTMLParser):
    test = 0
    inSidebar = False
    postsCategoryParser = PostsCategoryParser()
    result = dict()

    def parsePage(self, urll):
        self.url = urll
        data = urllib2.urlopen(urll)

        content = data.read().decode('utf-8')
        self.result = dict()
        self.feed(content)
        return self.result

    def handle_starttag(self, tag, attrs):
        if tag == "div" and attrs[0][0] == "class" and attrs[0][1] == "Sidebar":
            inSideBar = False
        if tag == "a" and attrs[0][0] == "href" and attrs[0][1].startswith("/category/"):
            self.postsCategoryParser.getPostsInCategoty(self.result, "http://aalmaan.blogfa.com/" , attrs[0][1])
