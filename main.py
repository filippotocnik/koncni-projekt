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

class RegistrationHandler(BaseHandler):
    def get(self):
        return self.render_template("register.html")

    def post(self):
        # pull info from input
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        email = self.request.get("email")
        originalno_geslo = self.request.get("password")
        repeat_password = self.request.get("repeat_password")

        first_name = cgi.escape(first_name)
        last_name = cgi.escape(last_name)
        email = cgi.escape(email)
        originalno_geslo = cgi.escape(originalno_geslo)
        repeat_password = cgi.escape(repeat_password)

        if originalno_geslo == repeat_password:
            # checking if passwords match
            User.ustvari(first_name, last_name, email, originalno_geslo)
        return self.render_template("login.html")


class LoginHandler(BaseHandler):
    def get(self):
        return self.render_template("login.html")

    def post(self):
        loged_in_user = User.gql("WHERE email='%s'" % self.request.get("email")).get()

        if User.preveri_geslo(self.request.get("password"), loged_in_user):
            self.create_cookie(user=loged_in_user)
            return self.render_template("home.html")
        else:
            self.write("NO!")

class NewMessageHandler(BaseHandler):
    def get(self):
        return self.render_template("new_message.html")

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        message_to = self.request.get("message_to")
        subject = cgi.escape(subject)
        content = cgi.escape(content)

        cookie_value = self.request.cookies.get("uid")
        user_id, _, _ = cookie_value.split(":")
        user_id = int(user_id)

        #receiver = User.gql("WHERE email='%s'" % message_to).get()
        receiver = User.gql("WHERE email='" + message_to + "'").get()
        receiver_id = receiver.key.id()
        message = Message(subject=subject, content=content, receiver_email=message_to, user_id=user_id, receiver_id=receiver_id)
        message.put()

        self.redirect("/show_message")

class ShowMessageHandler(BaseHandler):
    def get(self):

        cookie_value = self.request.cookies.get("uid")
        user_id, _, _ = cookie_value.split(":")
        user_id = int(user_id)
        user = User.get_by_id(int(user_id))
        user_email = user.email
        inbox = Message.gql("WHERE receiver_id=" + str(user_id)).order(-Message.nastanek).fetch()

        view_vars = {
            "inbox": inbox,
            "user_email": user_email,
        }

        return self.render_template("show_message.html", view_vars)

class EachMessageHandler(BaseHandler):
    def get(self, message_id):
        message = Message.get_by_id(int(message_id))

        view_vars = {
            "message": message,
        }

        return self.render_template("each_message.html", view_vars)

class EditMessageHandler(BaseHandler):
    def get(self, message_id):
        message = Message.get_by_id(int(message_id))

        view_vars = {
            "message": message,
        }

        return self.render_template("edit_message.html", view_vars)

    def post(self, message_id):
        message = Message.get_by_id(int(message_id))
        #message.ime= self.request.get("ime")
        message.email = self.request.get("email")
        message.content = self.request.get("sporocilo")
        message.put()

        self.redirect("/message/" + message_id)



app = webapp2.WSGIApplication([
    webapp2.Route('/', RegistrationHandler),
    webapp2.Route('/login', LoginHandler),
    webapp2.Route('/new_message', NewMessageHandler),
    webapp2.Route('/show_message', ShowMessageHandler),
    webapp2.Route('/each_message', EachMessageHandler),
], debug=True)


""""
Vprasanja:
- kaj je @classmethod v modelih?
- kako 'gledas' v bazo?
- kako jemljes iz baze?
- preverjanje gesla?

"""