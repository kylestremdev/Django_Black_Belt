from __future__ import unicode_literals

from django.db import models

import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def register(self, post_data):
        errors = []

        #name
        if len(post_data['name']) < 3:
            errors.append('Name must be at least 3 characters')
        elif len(post_data['name']) > 45:
            errors.append('Name must be under 45 characters')

        #username
        if len(post_data['username']) < 3:
            errors.append('Username must be at least 3 characters')
        elif len(post_data['username']) > 45:
            errors.append('Username must be under 45 characters')

        #password
        if len(post_data['password']) < 8:
            errors.append('Password must be at least 8 characters')
        elif post_data['password'] != post_data['password_confirmation']:
            errors.append('Passwords must match')

        if len(errors) > 0:
            return errors

        password = bcrypt.hashpw(post_data['password'].encode('utf-8'), bcrypt.gensalt())

        user = User.objects.create(
            name=post_data['name'],
            username=post_data['username'],
            password=password
        )

        return user

    def login(self, post_data):
        errors = []

        user = None
        #username
        if len(post_data['username']) < 1:
            errors.append("Username cannot be empty")
            return errors
        else:
            try:
                user = User.objects.get(username=post_data['username'])
            except:
                errors.append('Incorrect Username')
                return errors

        #password
        if bcrypt.hashpw(post_data['password'].encode('utf-8'), user.password.encode('utf-8')) == user.password:
            return user
        else:
            errors.append("Incorrect Password")
            return errors

class User(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
