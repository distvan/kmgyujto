import os
import webapp2
from xml.etree import ElementTree as ET
from model import quotations as QT

class QUploader(webapp2.RequestHandler):
    
    def upload(self):
        path = os.path.dirname(os.path.dirname((__file__))) + '/static/data/quotations.xml'
        tree = ET.parse(path)
        texts = tree.findall('saying')
        for item in texts:
            quotation = QT.Quotations()
            day = item.get('id')
            say = item.find('text').text
            author = item.find('author').text
            quotation.day = int(day)
            quotation.saying = say
            quotation.author = author
            quotation.put()
        self.response.out.write('Upload done.')