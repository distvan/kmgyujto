from google.appengine.ext import db
import datetime

# Store running distances per day, per user

class Quotations(db.Model):
    day = db.IntegerProperty()
    saying = db.StringProperty()
    author = db.StringProperty()
    
    def getTodaySaying(self):
        now = datetime.datetime.now()
        q = db.GqlQuery("SELECT * FROM Quotations where day=:1", now.day)
        return q.get()
