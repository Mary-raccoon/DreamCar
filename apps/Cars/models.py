from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')


class UserManager(models.Manager):
    def basic_validator(self, postdata):
        errors = {}
        if len(postdata['name']) < 3:
            errors['name'] = "Name should be at least 2 characters"
        elif not 'name' in errors and not re.match(NAME_REGEX, postdata['name']):
            errors['name'] = "Name must only contain letters"
        if not 'email' in errors and not re.match(EMAIL_REGEX, postdata['email']):
            errors['email'] = "Email is invalid"
        if len(postdata['password']) < 8:
            if len(postdata['password']) < 1:
                errors['password'] = "Password can't be blank"
            errors['password'] = "Password should be no fewer than 8 characters in length"
        if postdata['conf_password'] != postdata['password']:
            errors['conf_password'] = "Passwords do not match"
        return errors

    def login_validator(self, postdata):
        errors = {}
        if len(postdata['email1']) < 1:
            errors['email1'] = "Not a valid email"
        if len(User.objects.filter(email=postdata['email1'])) == 0:
            errors['email1'] = "Email does not exist. Register first!"
        if len(User.objects.filter(email=postdata['email1'])) == 1:
            password_hash = User.objects.get(email=postdata['email1']).password
            if bcrypt.checkpw(postdata['password1'].encode(), password_hash.encode()) == False:
                errors['password1'] = "Incorrect password. Try again!"
        return errors


class User(models.Model):
    name = models.CharField(max_length=255, blank=False)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __repr__(self):
        return "<User_object: {} {}>".format(self.name, self.email)


class CarManager(models.Manager):
    def car_validator(self, postdata):
        errors = {}
        if len(postdata['make']) < 3:
            errors['make'] = "Make should be at least 2 characters"
        return errors


class Car(models.Model):
    make = models.CharField(max_length=45)
    model = models.CharField(max_length=45)
    year = models.IntegerField()
    price = models.IntegerField()
    pic = models.CharField(max_length=45)
    desc = models.TextField()
    video = models.CharField(max_length=255)
    author = models.ForeignKey(User, related_name="cars", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="liked_cars")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
