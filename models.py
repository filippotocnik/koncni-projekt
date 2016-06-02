import hashlib
import hmac
import uuid
from google.appengine.ext import ndb

class User(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    sifrirano_geslo = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def ustvari(cls, ime, priimek, email, original_geslo):
        user = cls(first_name=ime, last_name=priimek, email=email,
                   sifrirano_geslo=cls.sifriraj_geslo(original_geslo=original_geslo))
        user.put()
        return user

    @classmethod
    def sifriraj_geslo(cls, original_geslo):
        salt = uuid.uuid4().hex
        sifra = hmac.new(str(salt), str(original_geslo), hashlib.sha512).hexdigest()
        return "%s:%s" % (sifra, salt)

    @classmethod
    def preveri_geslo(cls, original_geslo, user):
        sifra, salt = user.sifrirano_geslo.split(":")
        preverba = hmac.new(str(salt), str(original_geslo), hashlib.sha512).hexdigest()

        if preverba == sifra:
            return True
        else:
            return False

class Message(ndb.Model):
    subject = ndb.StringProperty()
    content = ndb.TextProperty()
    receiver_email = ndb.StringProperty()
    user_id = ndb.IntegerProperty()
    receiver_id = ndb.IntegerProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)



