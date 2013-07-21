import datetime
from google.appengine.ext import db

# Store running summary distances per week, per user

class TopWeeks(db.Model):
    fid = db.IntegerProperty()
    name = db.StringProperty()
    year = db.IntegerProperty()
    week = db.IntegerProperty()
    summary = db.FloatProperty()
    def getTopTen(self):
        now = datetime.datetime.now()
        week = now.isocalendar()[1]
        q = db.GqlQuery("SELECT * FROM TopWeeks WHERE year=:1 AND week=:2 ORDER BY summary DESC LIMIT 10", now.year, week)
        return q.fetch(10)

    def currWeek(self, fid, year, week):
        q = db.GqlQuery("SELECT * FROM TopWeeks WHERE fid=:1 AND year=:2 AND week=:3 ORDER BY summary DESC", fid, year, week)
        if q.count() > 0 :
            res = q.get()
        else:
            res = 0
        return res
    
class TopMonths(db.Model):
    fid = db.IntegerProperty()
    year = db.IntegerProperty()
    name = db.StringProperty()
    month = db.IntegerProperty()
    summary = db.FloatProperty()
    def getTopTen(self):
        now = datetime.datetime.now()
        q = db.GqlQuery("SELECT * FROM TopMonths WHERE year=:1 AND month=:2 ORDER BY summary DESC LIMIT 10", now.year, now.month)
        return q.fetch(10)
    
    def currMonth(self, fid, year, month):
        q = db.GqlQuery("SELECT * FROM TopMonths WHERE fid=:1 AND year=:2 AND month=:3 ORDER BY summary DESC", fid, year, month)
        if q.count() > 0 :
            res = q.get()
        else:
            res = 0
        return res
    
    def getMonthSummary(self, fid):
        now = datetime.datetime.now()
        q = db.GqlQuery("SELECT month, summary FROM TopMonths WHERE year=:1 AND fid=:2 ORDER BY month DESC", now.year, fid)
        return q.fetch(12) 
    
class TopYears(db.Model):
    fid = db.IntegerProperty()
    name = db.StringProperty()
    year = db.IntegerProperty()
    summary = db.FloatProperty()
    def getTopTen(self):
        now = datetime.datetime.now()
        q = db.GqlQuery("SELECT * FROM TopYears WHERE year=:1 ORDER BY summary DESC LIMIT 10", now.year)
        return q.fetch(10)
    
    def currYear(self, fid, year):
        q = db.GqlQuery("SELECT * FROM TopYears WHERE fid=:1 AND year=:2 ORDER BY summary DESC", fid, year)
        if q.count() > 0 :
            res = q.get()
        else:
            res = 0
        return res