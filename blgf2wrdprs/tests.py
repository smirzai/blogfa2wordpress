

from  exporter.exportBlogfa27 import extractSite
from  exporter.subjectParser import SubjectListParser

print ( "hello world")


parser = SubjectListParser()
(subjects, result) = parser.parsePage("http://aalmaan.blogfa.com")
print result['/post/48']
print subjects['/category/24']