#!/usr/bin/env python
import os
import jinja2
import webapp2
import hashlib
from models import User


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

class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

class LoginHandler(BaseHandler):
    def get(self):
        return self.render_template("login.html")

    def post(self):
        # pull info from input
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        email = self.request.get("email")
        password = self.request.get("password")
        repeat_password = self.request.get("repeat_password")


        if password == repeat_password:
            # checking if passwords match
            user = User(first_name=first_name, last_name=last_name, email=email, password=str(hashlib.sha512(password)))
            user.put()


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/login', LoginHandler),
], debug=True)
