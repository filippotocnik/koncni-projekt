#!/usr/bin/env python
import os
import jinja2
import webapp2
import hashlib
import cgi
import datetime
import hmac
import time
from secret import secret
from models import User, Message


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

    def create_cookie(self, user):
        # created cookie
        user_id = user.key.id()
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=10)
        expires_ts = int(time.mktime(expires.timetuple()))
        sifra = hmac.new(str(user_id), str(secret) + str(expires_ts), hashlib.sha1).hexdigest()
        value = "{0}:{1}:{2}".format(user_id, sifra, expires_ts)
        self.response.set_cookie(key="uid", value=value, expires=expires)

class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

class RegistrationHandler(BaseHandler):
    def get(self):
        return self.render_template("login.html")

    def post(self):
        # pull info from input
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        email = self.request.get("email")
        password = str(hashlib.sha512(self.request.get("password")))
        repeat_password = str(hashlib.sha512(self.request.get("repeat_password")))

        first_name = cgi.escape(first_name)
        last_name = cgi.escape(last_name)
        email = cgi.escape(email)
        password = cgi.escape(password)
        repeat_password = cgi.escape(repeat_password)

        if password == repeat_password:
            # checking if passwords match
            user = User(first_name=first_name, last_name=last_name, email=email, password=password)
            user.put()

class InboxHandler(BaseHandler):
    def get(self):
        if #kako preveriti password


        return self.render_template("inbox.html")

    def post(self):


class NewMessageHandler(BaseHandler):
    def get(self):
        return self.render_template("new_message.html")

    def post(self):
        receiver = self.request.get("message_to")
        subject = self.request.get("subject")
        message = self.request.get("memessage")

        message = Message(subject=subject, content=message, sender_id= , reciver_id= )



app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/login', RegistrationHandler),
    webapp2.Route('/inbox', InboxHandler),
    webapp2.Route('/newmessage', NewMessageHandler),
], debug=True)


""""
Vprasanja:
- kaj je @classmethod v modelih?
- kako 'gledas' v bazo?
- kako jemljes iz baze?
- preverjanje gesla?

"""