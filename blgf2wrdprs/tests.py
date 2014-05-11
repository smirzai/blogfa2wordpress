

from  exporter.exportBlogfa27 import extractSite
from  exporter.subjectParser import SubjectListParser

print ( "hello world")


parser = SubjectListParser()
result = parser.parsePage("http://aalmaan.blogfa.com")
print result