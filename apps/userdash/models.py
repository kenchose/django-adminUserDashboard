# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import logout
from django.contrib import messages
import bcrypt


class UserManager(models.Manager):
    def register(self, postData):
        error = []
        if len(postData['email']) < 1 or len(postData['first_name']) < 1 or len(postData['last_name']) < 1 or len(postData['password']) < 1:
            error.append("All fields must be filled")
        try:
            validate_email(postData['email'])
        except ValidationError as e:
            error.append("Email must be a valid email.")
        if len(postData['email']) < 6:
            error.append("Email must be more than 6 characters long.")
        if User.objects.filter(email__iexact=postData['email']):
            error.append('Email is already registered.')
        if not postData['first_name'].isalpha():
            error.append("First name cannnot contain numbers or special characters. ")
        if len(postData['first_name']) < 2:
            error.append("First name must be more than 2 characters.")
        if len(postData['last_name']) < 2:
            error.append("Last name must be more than 2 characters.")
        if len(postData['password']) < 8: #put in password must cocntain at least one special character, number, and upppercase letter
            error.append("Password must be more than 8 characters.")
        if postData['password'] != postData['password_confirmation']:
            error.append('Confirmatin password does not match.')
        return error


    def newUser(self, postData):
        hashed_pw=bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        new_user = User.objects.create(email = postData['email'], first_name = postData['first_name'], last_name = postData['last_name'], password = hashed_pw)
        if new_user.id == 1:
            new_user.admin = "Admin"
            new_user.save()
        return new_user   


    def loginValid(self,postData):
        error = []
        retrieved_users = User.objects.filter(email=postData['email'])
        if len(retrieved_users) > 0:
            retrieved_user = retrieved_users[0]
            if not bcrypt.checkpw(postData['password'].encode(), retrieved_user.password.encode()):
                error.append("Invalid email/password")
                return error
        else:
            error.append("Email is not registered.")
            return error


    def loginUser(self, postData):
        error = []
        retrieved_users = User.objects.filter(email=postData['email'])
        if len(retrieved_users) > 0:
            retrieved_user = retrieved_users[0]
            if bcrypt.checkpw(postData['password'].encode(), retrieved_user.password.encode()):
                if retrieved_user.id == 1:
                    retrieved_user.admin = "Admin"
                    retrieved_user.save()
                    return retrieved_user
                else:
                    return retrieved_user
            else:
                error.append("Email/password is invalid.")
                return error
        else:
            error.append("Email not registered.")
            return error


      

class User(models.Model):
    email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    admin = models.CharField(max_length=100, default="Normal")
    description = models.CharField(max_length=255, blank=True)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __repr__(self):
        return '<User: {} {} {} {}>'.format(self.first_name, self.last_name, self.email, self.admin)

class Message(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name='message_by')
    recipient = models.ForeignKey(User, related_name="message_to")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __repr__(self):
        return '<Message: {} {} said {}.>'.format(self.user.first_name, self.user.last_name, self.content, self.message.first_name) 

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name = "replied_by")
    reply = models.ForeignKey(Message, related_name = "message")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __repr__(self):
        return '<Comment: {} replied {} to {} made by {}'.format(self.user__first_name, self.content, self.reply__content, self.reply__content__first_name)
