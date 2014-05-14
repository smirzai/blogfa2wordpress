#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Name:        Export Blogfa
# Purpose:      Export Blogfa to wordpress readable file
#
# Author:      Saeid Mirzaei
#
# Created:     21.04.2013
# Copyright:   (c) Saeid Mirzaei 2013
#-------------------------------------------------------------------------------
from HTMLParser import HTMLParser
import urllib2
import re
from datetime import datetime
from  jalali import JalaliToGregorian
import codecs
from  subjectParser import SubjectListParser

smileys = (':)', # smile                1
           ':(', # sad                  2
           ';)', # wink                 3
           ':P', # raz                  4
           ':lol:', # lol               5
           ':cry:', #cry                6
           '',   # heart                7
           ':oops:', # oops, shy        8
           '',  # tongue                9
           '',  # kiss                  10
           '',  #broken heart           11
           ':shock:', #shock            12
           ':mad:', # mad               13
           ':cool:', # cool             14
           ':neutral:', # nutral        15
           ':???:', # ???               16
           ':evil:', # evil             17
           '', # bye                    18
           ':mrgreen:', # ill           19
           '' # flower                  20
           )


smileyPattern = re.compile('<img src="http://www.blogfa.com/cmt/images/(\d{1,2}).gif">')
def convertSmileys(str):
    m = re.search(smileyPattern, str)

    while m != None:
        sm = smileys[int(m.group(1))-1]
        found = m.group(0)
        str = str.replace(found, ' ' + sm + ' ')
        m = re.search(smileyPattern, str)

    return str;



outFile = ""

def outputStart(title, subjects):
    outFile.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
    outFile.write('<rss version="2.0\n');
    outFile.write('    xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"\n');
    outFile.write('    xmlns:content="http://purl.org/rss/1.0/modules/content/"\n');
    outFile.write('    xmlns:wfw="http://wellformedweb.org/CommentAPI/"\n');
    outFile.write('    xmlns:dc="http://purl.org/dc/elements/1.1/"\n');
    outFile.write('    xmlns:wp="http://wordpress.org/export/1.2/"\n');
    outFile.write('>\n');



    outFile.write('<channel>\n');
    outFile.write('	<title>' + title + '</title>\n')
    outFile.write('    <link>http://blog.saeidmirzaei.com</link>\n')
    outFile.write('    <description>Just another WordPress site</description>\n')
    outFile.write('    <pubDate>Sun, 21 Apr 2013 11:12:28 +0000</pubDate>\n')
    outFile.write('    <language>en-US</language>\n')
    outFile.write('    <wp:wxr_version>1.2</wp:wxr_version>\n')
    outFile.write('    <wp:base_site_url>http://blog.saeidmirzaei.com</wp:base_site_url>\n')
    outFile.write('    <wp:base_blog_url>http://blog.saeidmirzaei.com</wp:base_blog_url>\n')

    outFile.write('    <wp:author><wp:author_id>1</wp:author_id><wp:author_login>admin</wp:author_login><wp:author_email>smirzai@gmail.com</wp:author_email><wp:author_display_name><![CDATA[admin]]></wp:author_display_name><wp:author_first_name><![CDATA[]]></wp:author_first_name><wp:author_last_name><![CDATA[]]></wp:author_last_name></wp:author>\n')
    for subject in subjects:
        outFile.write('    <wp:category><wp:term_id>' + subject + '</wp:term_id><wp:category_nicename>' + subjects[subject] + '</wp:category_nicename><wp:category_parent></wp:category_parent><wp:cat_name><![CDATA[' + subjects[subject] + ']]></wp:cat_name></wp:category>\n')

    outFile.write('    <generator>http://wordpress.org/?v=3.5.1</generator>\n')


def outputEnd():
    outFile.write('</channel>\n');
    outFile.write('</rss>\n');
    outFile.flush()

class PostListParser(HTMLParser):
    isInTitle = 0
    titleWritten =  0
    postTitle = ""
    isInResult = 0
    resultDepth = 0
    url = ""
    divDepth = 0
    seenSpan = 0
    isInNavBar = 0
    navBarDepth = 0
    next = ""

  
    def setOutFile(self, name):
        global outFile
        outFile = codecs.open(name, "w",  'utf-8')


    def parsePage(self, urll, subjects, subjectMapping):
        self.subjects = subjects
        self.subjectMapping = subjectMapping
        self.url = urll
        u = urll + "/posts/"
        while (True):
            data = urllib2.urlopen(u)
            content = data.read().decode('utf-8')
            self.feed(content)
            if (not self.next):
                break;
            u = urll + "/posts/" + self.next
            self.next = ""
        outputEnd()
        outFile.close

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.isInTitle = 1
            return;

        if tag == "div":
            self.divDepth += 1


        if tag== "div" and not self.isInResult:
             if attrs:
                tagsWithHref =[x[1] for x in attrs if x[0]=='id' and x[1]=="result"]
                if tagsWithHref:
                    self.isInResult = 1
                    self.resultDepth = self.divDepth
                    return

        if tag== "div" and  self.isInResult:
                tagsWithHref =[x[1] for x in attrs if x[0]=='id' and x[1]=="navbar"]
                if tagsWithHref:
                    self.isInNavBar = 1
                    self.navBarDepth = self.divDepth
                    return


        if tag == "a" and self.seenSpan and self.isInNavBar:
            if attrs:
                tagsWithId =[x[1] for x in attrs if x[0]=='href']
                if tagsWithId:
                    self.next = tagsWithId[0]
                    self.seenSpan = 0
                    self.isInNavBar = 0

                    return


        if tag =="a" and self.isInResult:
            if attrs:
                tagsWithId =[x[1] for x in attrs if x[0]=='href']
                if tagsWithId:

                    if not tagsWithId[0].startswith("?p="):
                        MyHTMLParser().parsePage(self.url, tagsWithId[0], self.subjects, self.subjectMapping)

                    return

        if tag == "span" and self.isInNavBar:
            self.seenSpan = 1
            return




    def handle_data(self, data):
        if self.isInTitle:
            self.postTitle = data;
            if (not self.titleWritten):
                outputStart(self.postTitle, self.subjects)
                self.titleWritten = 1


    def handle_endtag(self, tag):
        if tag == "title":
            self.isInTitle = 0
            return

        if tag == "div":
            if self.divDepth == self.resultDepth:
                self.isInResult = 0
            if self.divDepth == self.navBarDepth:
                self.isInNavBar = 0

        if tag =="div":
            self.divDepth -= 1



class CommentParser(HTMLParser):
    commentId = 1
    commentAuthor = ""
    commentDate = ""
    commentAuthorURL = ""
    commentBody = ""

    divDepth = 0

    isInCommentBox = 0
    isInCommentAuthor = 0
    isInCommentDate=0
    isInCommentBody=0
    isInNavbar = 0
    seenSpan= 0
    next = ""

    levelCommentBox = 0



    def handle_starttag(self, tag, attrs):


        if not self.isInCommentBox and tag == "div":
            if attrs:
                tagsWithBox =[x[1] for x in attrs if x[0]=='class' and x[1]=='box']
                if tagsWithBox:
                    self.isInCommentBox = 1
                    self.levelCommentBox = self.divDepth
                    return

        if not self.isInCommentAuthor and self.isInCommentBox and tag == "div":
            if attrs:
                tagsWithAuthor =[x[1] for x in attrs if x[0]=='class' and x[1]=='author']
                if tagsWithAuthor:
                    self.isInCommentAuthor = 1
                    return

        if not self.isInCommentDate and self.isInCommentBox and tag == "div":
            if attrs:
                tagsWithDate =[x[1] for x in attrs if x[0]=='class' and x[1]=='date']
                if tagsWithDate:
                    self.isInCommentDate = 1
                    return

        if not self.isInCommentBody and self.isInCommentBox and tag == "div":
            if attrs:
                tagsWithBody =[x[1] for x in attrs if x[0]=='class' and x[1]=='body']
                if tagsWithBody:
                    self.isInCommentBody = 1
                    return

        if self.isInCommentAuthor and tag == 'a':
            if attrs:
                tagsWithLink =[x[1] for x in attrs if x[0]=='href' ]
                if tagsWithLink:
                    self.commentAuthorURL = tagsWithLink[0]
                    return


        if self.isInCommentBody:
            self.commentBody+=   "<%s" % (tag,)
            if attrs:
                self.commentBody += " " + " ".join('%s="%s"' % (k, v) for k, v in attrs)
            self.commentBody += ">"

        if tag == "div":
            self.divDepth += 1


        if self.isInNavbar and tag == "span":
            self.seenSpan = 1
            return

        if self.isInNavbar and self.seenSpan and tag == "a" and not self.next:
            if attrs:
                tagsWithA =[x[1] for x in attrs if x[0]=='href']
                if tagsWithA:
                    self.next = tagsWithA[0]


        if tag == "div":
            if attrs:
                tagsWithId =[x[1] for x in attrs if x[0]=='id' and x[1] == "navbar"]
                if tagsWithId:
                    self.isInNavbar = 1




    def convertCommentDate(self, dt):
        months=(u'فروردین', u'اردیبهشت', u'خرداد', u'تیر', u'مرداد', u'شهریور', u'مهر', u'آبان', u'آذر', u'دی', u'بهمن', u'اسفند')
        dt = dt.translate(dict((ord(x), y) for (x, y) in zip('۰۱۲۳۴۵۶۷۸۹', '0123456789')))
        tokens = re.split(' ', dt)
        if len(tokens) == 6:
            tokens = tokens[1:]
        shday = tokens[1]
        shyear = tokens[3]

        shMonth = months.index(tokens[2]) + 1
        dc = JalaliToGregorian(int(shyear), int(shMonth), int(shday))
        tm = tokens[4]

        return str(int(dc.gyear // 1)) + '-' + str(int(dc.gmonth // 1)) + '-' + str(int(dc.gday)) + ' ' + tm + ':00'



    def outputComment(self, author, authorUrl, date, body):
        outFile.write('        <wp:comment>\n');
        outFile.write('             <wp:comment_id>%s</wp:comment_id>\n' % (str(self.commentId),));
        outFile.write('             <wp:comment_author><![CDATA[%s]]></wp:comment_author>\n' % (author,));
        outFile.write('             <wp:comment_author_email/>\n');
        outFile.write('             <wp:comment_author_url>%s</wp:comment_author_url>\n' % (authorUrl,));
        outFile.write('             <wp:comment_author_IP></wp:comment_author_IP>\n');
        outFile.write('             <wp:comment_date>%s</wp:comment_date>\n' % self.convertCommentDate(self.commentDate,));
        outFile.write('             <wp:comment_date_gmt>%s</wp:comment_date_gmt>\n' % self.convertCommentDate(self.commentDate,));
        outFile.write('             <wp:comment_content><![CDATA[%s]]></wp:comment_content>\n' % (convertSmileys(body),));
        outFile.write('             <wp:comment_approved>1</wp:comment_approved>\n');
        outFile.write('             <wp:comment_type/>\n');
        outFile.write('             <wp:comment_parent>0</wp:comment_parent>\n');
        outFile.write('             <wp:comment_user_id>0</wp:comment_user_id>\n');
        outFile.write('        </wp:comment>\n');
        self.commentId +=1






    def handle_endtag(self, tag):
        if self.isInCommentBox and tag == "div" and self.divDepth == self.levelCommentBox:
            self.isInCommentBox = 0
            self.outputComment(self.commentAuthor,self.commentAuthorURL,self.commentDate, self.commentBody)
            self.commentAuthor = ''
            self.commentAuthorURL = ''
            self.commentBody=''
            self.commentDate=''
            return

        if self.isInCommentAuthor and tag =="div":
            self.isInCommentAuthor = 0
            return

        if self.isInCommentDate and tag =="div":
            self.isInCommentDate = 0
            return

        if self.isInCommentBody and tag =="div":
            self.isInCommentBody = 0
            return
        if self.isInCommentBody:
            self.commentBody +=  "</%s>" % (tag)

        if tag=="div":
            self.divDepth -= 1

        if tag == "div" and self.isInNavbar:
            self.isInNavbar = 0


    def handle_data(self, data):
        if self.isInCommentAuthor:
            self.commentAuthor = data
            return
        if self.isInCommentDate:
            self.commentDate = data
            return
        if self.isInCommentBody:
            self.commentBody += data


class MyHTMLParser(HTMLParser):
    global outFile;
 
    commentParser = CommentParser()

# date
    blogTitle = ""
    blogId = ""
    postTitle = ""
    postUrl = ""
    postContent = ""
    postInfo =""
    postDateTime = "";


    url =""
    divDepth = 0

    record = ""

    isInPost = 0
    postLevel = 0
    isInCnt = 0
    cntLevel = 0
    isInInfo = 0
    infoLevel = 0
    isInTitle = 0
    isInPostTitle = 0
    isInInfo = 0
    isInScript = 0



    def getBlogIdFromInfo(self, info):
        m = re.search('strBlogId="(.*)";', info)
        if (m):
            self.blogId=m.group(1);


    def getDateFromPostInfo(self, info):
        m = re.search("[0-9]{4}/[0-9]{1,2}/[0-9]{1,2}", info)
        if (not m):
           print("no input")
           return
        else:
            dateStr = m.group(0);


        m = re.search("[0-9]{1,2}:[0-9]{1,2}", info)

        if (not m):
           print("no input")
           return
        else:
            timeStr = m.group(0)


        self.postDateTime = datetime.strptime(dateStr + ' ' + timeStr, '%Y/%m/%d %H:%M')






    def  outputPost(self, postTitle, postContent, postUrl, postDateTime, subjects, subjectMapping):
        if (not postDateTime):
          postDateTime = datetime.today()
        postId =postUrl[6:-5]
        dayNames = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
        monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
        outFile.write('    <item>\n')
        outFile.write('        <title>%s</title>\n' % (postTitle,))
        outFile.write('        <link>%s</link>\n' % (self.url +  postUrl,))
        outFile.write('        <pubDate>%s, %s %s %s +0000</pubDate>\n' % (dayNames[int(postDateTime.strftime("%w"))],postDateTime.strftime("%d"), monthNames[int(postDateTime.strftime("%m"))-1], postDateTime.strftime(" %Y  %H:%M:%S")),)
        outFile.write('        <dc:creator>admin</dc:creator>\n')
        outFile.write('        <guid isPermaLink="false">%s</guid>\n' % (self.url + postUrl,))
        outFile.write('        <description></description>\n')
        outFile.write('        <content:encoded><![CDATA[%s]]></content:encoded>\n' % (convertSmileys(postContent),))
        outFile.write('        <excerpt:encoded><![CDATA[]]></excerpt:encoded>\n')
        outFile.write('        <wp:post_id>%s</wp:post_id>\n' % (postId,))
        outFile.write('        <wp:post_date>%s</wp:post_date>\n' % postDateTime.strftime("%Y-%m-%d %H:%M:%S"))
        outFile.write('        <wp:post_date_gmt>%s</wp:post_date_gmt>\n'% postDateTime.strftime("%Y-%m-%d %H:%M:%S"))
        outFile.write('        <wp:comment_status>open</wp:comment_status>\n')
        outFile.write('        <wp:ping_status>open</wp:ping_status>\n')
        outFile.write('        <wp:post_name>%s</wp:post_name>\n' % (postTitle,))
        outFile.write('        <wp:status>publish</wp:status>\n')
        outFile.write('        <wp:post_parent>0</wp:post_parent>\n')
        outFile.write('        <wp:menu_order>0</wp:menu_order>\n')
        outFile.write('        <wp:post_type>post</wp:post_type>\n')
        outFile.write('        <wp:post_password></wp:post_password>\n')
        outFile.write('        <wp:is_sticky>0</wp:is_sticky>\n')


        if postUrl[6:-5] in self.subjectMapping:
            for subjectNumber in self.subjectMapping[postUrl[6:-5]]:
                subjectTitle = self.subjects[subjectNumber]
                outFile.write('        <category domain="category" nicename="' + subjectTitle + '"><![CDATA[' + subjectTitle + ']]></category>\n')


        curl =self.url + "/comments/?blogid="  +self.blogId + "&postid=" + postId
        while (True):
            commentsurl = urllib2.urlopen(curl)




            commentContent = commentsurl.read().decode('utf-8')
            self.commentParser.feed(commentContent)
            curl = self.commentParser.next
            if (curl):
                curl = self.url + "/comments/" +curl
                self.commentParser.next=""
                self.commentParser.seenSpan = 0
            else:
                break



        outFile.write('    </item>\n')
        outFile.flush()






    def handle_starttag(self, tag, attrs):
        if self.isInCnt:
            tagsWithId =[x[1] for x in attrs if x[0]=='id' and x[1] == "postdesc"]
            if (tagsWithId):
                self.isInInfo = 1
                self.infoLevel = self.divDepth
                self.isInCnt = 0
                self.postContent = self.record
                self.record = ""

                return


            self.record +=   "<%s" % (tag,)
            if attrs:
                self.record += " " + " ".join('%s="%s"' % (k, v) for k, v in attrs)
            self.record += ">"
            return

        if not self.isInTitle and tag == "title":
            self.isInTitle = 1
            return

        if self.isInPost and self.divDepth == self.postLevel  and tag == "a":
            if attrs:
                tagsWithHref =[x[1] for x in attrs if x[0]=='href']
                if tagsWithHref:
                    self.postUrl = tagsWithHref[0]
                    self.isInPostTitle = 1
            return


        if tag=="script" and self.divDepth == 0:
            self.isInScript = 1

        if tag != "div":
            return

        self.divDepth += 1

        cls =""

        tagsWithClass =[x[1] for x in attrs if x[0]=='class']
        if (not tagsWithClass):
            tagsWithId =[x[1] for x in attrs if x[0]=='id']
            if (tagsWithId):
                cls = tagsWithId[0]
            else:
              return
        else:
          cls = tagsWithClass[0]


        if cls == "post":
            self.isInPost = 1
            self.postLevel = self.divDepth
        elif cls == "cnt" :
            self.isInCnt = 1
            self.cntLevel = self.divDepth
        elif cls == "info" :
            self.isInInfo = 1
            self.infoLevel = self.divDepth




    def handle_endtag(self, tag):

        if tag == "title":
            isInTitle = 0
            return

        if tag == "div" and self.isInCnt and self.divDepth == self.cntLevel:
            self.isInCnt = 0
            self.postContent = self.record
            self.record = ""
            return

        if self.isInCnt:
            self.record +=  "</%s>" % (tag)
            return


        if self.isInPostTitle and self.divDepth == self.postLevel  and tag == "a":
            self.isInPostTitle = 0
            return

        if self.isInScript and tag == "script" and self.divDepth == 0:
            self.isInScript = 0



        if tag != "div":
           return


        if self.isInInfo and self.divDepth == self.infoLevel:
            self.isInInfo = 0

            self.getDateFromPostInfo(self.postInfo)
            self.postInfo = ""

            self.outputPost(self.postTitle, self.postContent, self.postUrl, self.postDateTime, self.subjects, self.subjectMapping)

        elif self.isInPost and self.postLevel == self.divDepth:
            self.isInPost = 0
        self.divDepth -= 1


    def __init__(self):
        HTMLParser.__init__(self)

    def handle_data(self, data):

        if self.isInTitle==1 and self.blogTitle == "":
            self.blogTitle = data
#            outputStart(self.blogTitle)
            return

        if self.isInPostTitle:
            self.postTitle = data
            return

        if self.isInCnt:
            self.record += data
            return

        if self.isInInfo:
            self.postInfo += data
            return

        if self.isInScript:
            self.getBlogIdFromInfo(data)


    def  parsePage(self, urll, post, subjects, subjectMapping):
        self.subjectMapping = subjectMapping
        self.subjects = subjects

        self.url = urll

        data = urllib2.urlopen(urll + post)
        content = data.read().decode('utf-8')




        self.feed(content)





def extractSite(name, fileName):
    siteFullName = 'http://' + name + ".blogfa.com";

    subjectParser = SubjectListParser()
    (subjects, result) = subjectParser.parsePage(siteFullName)


    parser = PostListParser()
    parser.setOutFile(fileName + ".xml")
    parser.parsePage(siteFullName, subjects, result)


