#!/usr/bin/env python
import webapp2
import jinja2
from model import quotations as QT
from model import topweeks as TW

# This controller handles the
# generation of the front page.

class PageHandler(webapp2.RequestHandler):
    
    def index(self):
        q = QT.Quotations()
        result = q.getTodaySaying()
        template_values = {
                'text' : result.saying,
                'author' : result.author,
                'topweek' : TW.TopWeeks().getTopTen(),
                'topmonth' : TW.TopMonths().getTopTen(),
                'topyear' : TW.TopYears().getTopTen()
        }
        self.render_template(self,'base.html', template_values)
    
    def gamerules(self):
        self.render_template(self,'gamerules.html',{})
    
    def joinus(self):
        self.render_template(self,'joinus.html',{})
    
    def render_template(self, h, filename, template_vars):
        jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader('view'))
        template = jinja_environment.get_template(filename)
        h.response.out.write(template.render(template_vars))