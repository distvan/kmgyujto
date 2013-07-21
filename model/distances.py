import datetime
from google.appengine.ext import db
from model import topweeks as tw
from datetime import date, timedelta

# Store running distances per day, per user

class Distances(db.Model):
    fid = db.IntegerProperty()
    date = db.DateProperty(auto_now_add=True)
    distance = db.FloatProperty()
    name = db.StringProperty()
    def isExisting(self, date, fid):
        q = db.GqlQuery("SELECT * FROM Distances WHERE date=:1 AND fid=:2", date, fid)
        if q.count() > 0: return True
        else: return False
        
    def getCurrentWeekDistances(self):
        now = datetime.datetime.now()
        week = now.isocalendar()[1]
        wd = self.get_week_days(now.year, week)
        q = db.GqlQuery("SELECT * FROM Distances WHERE date>=:1 AND date<=:2 AND fid=:3", wd[0], wd[1], self.fid)
        return q.fetch(7)
    
    #handle top lists summary
    def save(self):
        #add distance
        self.put()
        #add top week summary
        weeknum = self.date.isocalendar()[1]
        weeks = tw.TopWeeks()
        weeks.fid = self.fid
        weeks.year = self.date.year
        weeks.week = weeknum
        weeks.name = self.name
        currWeek = weeks.currWeek(self.fid, self.date.year, weeknum)
        if currWeek != 0:
            currWeek.summary = currWeek.summary + self.distance
            currWeek.name = self.name
            currWeek.put()
        else:
            weeks.summary = self.distance
            weeks.put()
        #add top month summary
        months = tw.TopMonths()
        months.fid = self.fid
        months.year = self.date.year
        months.name = self.name
        months.month = self.date.month
        currMonth = months.currMonth(self.fid, self.date.year, self.date.month)
        if currMonth != 0:
            currMonth.summary = currMonth.summary + self.distance
            currMonth.name = self.name
            currMonth.put()
        else:
            months.summary = self.distance
            months.put()
        #add top year summary
        years = tw.TopYears()
        years.fid = self.fid
        years.year = self.date.year
        years.name = self.name
        currYear = years.currYear(self.fid, self.date.year)
        if currYear != 0:
            currYear.summary = currYear.summary + self.distance
            currYear.name = self.name
            currYear.put()
        else:
            years.summary = self.distance
            years.put()
    
    def get_week_days(self, year, week):
        d = date(year,1,1)
        if(d.weekday()>3):
            d = d+timedelta(7-d.weekday())
        else:
            d = d - timedelta(d.weekday())
        dlt = timedelta(days = (week-1)*7)
        return d + dlt,  d + dlt + timedelta(days=6)
    
    def delDistance(self):
        q = db.GqlQuery("SELECT * FROM Distances WHERE date=:1 AND fid=:2", self.date, self.fid)
        distance = q.get()
        km = distance.distance
        distance.delete()
        #remove top week summary
        weeknum = self.date.isocalendar()[1]
        weeks = tw.TopWeeks()
        weeks.fid = self.fid
        weeks.year = self.date.year
        weeks.week = weeknum
        currWeek = weeks.currWeek(self.fid, self.date.year, weeknum)
        currWeek.summary = currWeek.summary - km
        currWeek.put()
        #rempove top month summary
        months = tw.TopMonths()
        months.fid = self.fid
        months.year = self.date.year
        months.month = self.date.month
        currMonth = months.currMonth(self.fid, self.date.year, self.date.month)
        currMonth.summary = currMonth.summary - km
        currMonth.put()
        #remove top year summary
        years = tw.TopYears()
        years.fid = self.fid
        years.year = self.date.year
        currYear = years.currYear(self.fid, self.date.year)
        currYear.summary = currYear.summary - km
        currYear.put()
        
    def getMonthSummary(self, fid):
        month = tw.TopMonths()
        months = month.getMonthSummary(fid)
        return months