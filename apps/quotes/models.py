# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validate_reg(self, postData):
        errors = []
        if len(postData['name']) < 2:
            errors.append("Name must be at least 2 characters long")
        if len(postData['alias']) < 1:
            errors.append("Alias is required")
        if len(postData['email']) < 1:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append("Please provide a valid email address")
        if len(postData['password']) < 8:
            errors.append("Password must be at least 8 characters in length")
        if len(postData['confirm_pass']) < 1:
            errors.append("Please confirm your password")
        elif postData['password'] != postData['confirm_pass']:
            errors.append("Passwords do not match")
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors.append("Please check your information and try again, or login if you already have an account.")
        if len(errors) > 0:
            return (False, errors)
        else: 
            pw_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            new_user = User.objects.create(name=postData['name'], alias=postData['alias'], email=postData['email'], password=pw_hash)
            return (True, new_user)

    def validate_login(self, postData):
        errors = []
        if len(postData['email']) < 1:
            errors.append("Please provide your email address")
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append("Please provide a valid email address")
        if len(postData['password']) < 1:
            errors.append("Please provide your password")  
        if len(User.objects.filter(email=postData['email'])) == 0:
            errors.append("Unable to verify email/password combination. Please try again or register if you do not have an account")       
        elif not bcrypt.checkpw(postData['password'].encode(), User.objects.get(email=postData['email']).password.encode()):
            errors.append("Unable to verify email/password combination. Please try again or register if you do not have an account")
        if len(errors) > 0:
            return (False, errors)
        else:
            user = User.objects.get(email=postData['email'])
            return(True, user)

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __str__(self):
        return self.name

class QuoteManager(models.Manager):
    def validate_quote(self, postData, user_id):
        errors = []
        if len(postData['quoted']) < 3:
            errors.append("Quoted By field must be 3+ characters in length")
        if len(postData['quote']) < 10:
            errors.append("Message field must be 10+ characters in length")
        if len(errors) > 0:
            print errors
            return (False, errors)
        else:
            quote = Quote.objects.create(quoted=postData['quoted'], quote=postData['quote'], contributor=User.objects.get(id=user_id))
            return (True, quote)



class Quote(models.Model):
    quoted = models.CharField(max_length=255)
    quote = models.TextField()
    contributor = models.ForeignKey(User, related_name="quotes")
    favorites = models.ManyToManyField(User, related_name="faves")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = QuoteManager()

    def __str__(self):
        return self.quote

