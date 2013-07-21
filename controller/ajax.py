#!/usr/bin/env python
# -*- coding: utf8 -*- 

import time
import datetime
import webapp2
import json
import jinja2
from model import distances as dis

class Request(webapp2.RequestHandler):
    
    def addDistance(self):
        date = self.request.get('date')
        fid = int(self.request.get('fid'))
        distance = self.request.get('distance')
        name = self.request.get('name')
        now = datetime.datetime.now()
        weeknow = now.isocalendar()[1]
        year = int(date[:4])
        month = int(date[5:7])
        day = int(date[8:])
        dt = datetime.date(year, month, day)
        weekinput = dt.isocalendar()[1]
        error = ''
        response_data = {}
        response_data['success'] = ""
        if self.isRightDateFormat(date) == False : 
            error = "Nem megfelelő dátum formátum!"
        if self.isNumber(distance) == False : 
            error = error + "Nem megfelelő km formátum!"
        if self.isNumber(distance) == True and float(distance)<=0 : 
            error = error + "Nem megfelelő km formátum!"
        if self.isNumber(fid) == False : 
            error = error + "Nem megfelelő Facebook azonosító!"
        if weeknow != weekinput: 
            error = error + "Távot csak az aktuális hétre lehet rögzíteni!"
        if len(error) == 0 : 
            d = dis.Distances()
            if d.isExisting(dt, fid) == False:
                d.fid = int(fid)
                d.date = dt
                d.distance = float(distance)
                d.name = name
                d.save()
                response_data['success'] = "Sikeres mentés!"
            else:
                error = "Erre a napra már van rögzített km!"
        response_data['error'] = error
        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        self.response.write(json.dumps(response_data))
        
    #check input is number 
    def isNumber(self, s):
        try:
            float(s) # for int, long and float
        except ValueError:
            try:
                complex(s) # for complex
            except ValueError:
                return False
        return True

    #check valid yy-mm-dd format
    def isRightDateFormat(self, string): 
        try:
            time.strptime(string, '%Y-%m-%d')
            return True
        except:
            return False

    def getWeeklyList(self):
        fid = self.request.get('fid')
        distances = dis.Distances()
        distances.fid = int(fid)
        myDistList = distances.getCurrentWeekDistances()
        jinja_environment=jinja2.Environment(autoescape=True,loader=jinja2.FileSystemLoader('view'))
        template = jinja_environment.get_template('mydistances.html')
        template_values = {
            'weeklyDistances' : myDistList, 
            'fid' : distances.fid 
        }
        self.response.out.write(template.render(template_values))

    def deleteDistance(self):
        date = self.request.get('date')
        distances = dis.Distances()
        year = int(date[:4])
        month = int(date[5:7])
        day = int(date[8:])
        dt = datetime.date(year, month, day)
        distances.date = dt
        distances.fid = int(self.request.get('fid'))
        distances.delDistance()
        self.response.out.write('OK')

    def getMonthSummary(self):
        fid = int(self.request.get('fid'))
        distances = dis.Distances()
        monthSummary = distances.getMonthSummary(fid)
        jinja_environment=jinja2.Environment(autoescape=True,loader=jinja2.FileSystemLoader('view'))
        template = jinja_environment.get_template('monthsummary.html')
        now = datetime.datetime.now()
        template_values = {
            'monthSummary' : monthSummary,
            'year' : now.year
        }
        self.response.out.write(template.render(template_values))