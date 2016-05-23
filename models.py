from google.appengine.ext import ndb

class User(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.EmailProperty()
    password = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

class Message(ndb.Model):
    subject = ndb.StringProperty()
    content = ndb.TextProperty()
    sender_id = ndb.IntegerProperty()
    receiver_id = ndb.IntegerProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)