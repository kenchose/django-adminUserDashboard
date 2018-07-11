# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
import bcrypt


class UserManager(models.Manager):
    def register(self, postData):
        error = []
        try:
            validate_email(postData['email'])
        except ValidationError as e:
            error.append("Email must be a valid email.")
        if len(postData['email']) < 1 or len(postData['first_name']) < 1 or len(postData['last_name']) < 1 or len(postData['password']) < 1:
            error.append("All fields must be filled")
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

    def adminAddUserVal(self, postData):
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
        if len(postData['password']) < 8: 
            error.append("Password must be more than 8 characters.")
        if postData['password'] != postData['password_confirmation']:
            error.append('Confirmatin password does not match.')
        return error


    def adminNewUser(self, postData):
        new_user = User.objects.create(email = postData['email'], first_name = postData['first_name'], last_name = postData['last_name'], password = postData['password'])
        hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        new_user.admin = "Normal"
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
                if  retrieved_user.id == 1:
                    retrieved_user.admin = "Admin"
                    retrieved_user.save()
                return retrieved_user
            else:
                error.append("Email/password is invalid.")
                return error
        else:
            error.append("Email not registered.")
            return error


    def editInfoVal(self, postData, user):
        error = []
        if len(postData['email']) < 1 or len(postData['first_name']) < 1 or len(postData['last_name']) < 1:
            error.append("All fields must be filled")
        try:
            validate_email(postData['email'])
        except ValidationError as e:
            error.append("Email must be a valid email.")
        if len(postData['email']) < 6:
            error.append("Email must be more than 6 characters long.")
        # if User.objects.filter(email__iexact=postData['email']).exclude(user.email):
        #     error.append('Email is already registered.')
        if not postData['first_name'].isalpha():
            error.append("First name cannnot contain numbers or special characters. ")
        if len(postData['first_name']) < 2:
            error.append("First name must be more than 2 characters.")
        if len(postData['last_name']) < 2:
            error.append("Last name must be more than 2 characters.")
        return error


    def editInfo(self, postData, curr_user):
        user = User.objects.get(id=curr_user.id)
        user.email = postData['email']
        user.first_name = postData['first_name']
        user.last_name = postData['last_name']
        user.save()
        return user


    def passVal(self, postData):
        error = []
        if len(postData['password']) < 8: 
            error.append("Password must be more than 8 characters.")
        if postData['password'] != postData['password_confirmation']:
            error.append('Confirmatin password does not match.')
        return error


    def newPass(self, postData, curr_user):
        user = User.objects.get(id=curr_user.id)
        hashed_pw=bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        user.password = hashed_pw
        user.save()
        return user


    def userValDesc(self, postData, curr_user):
        error = []
        if len(postData['description']) < 1:
            error.append("Description field must contain at least one character")
        return error


    def userDesc(self, postData, curr_user):
        user = User.objects.get(id=curr_user.id)
        user.description = postData['description']
        user.save()
        return user


    def adminInfoVal(self, postData, user):
        user_update = User.objects.get(id=user.id)
        error = []
        if len(postData['email']) < 1 or len(postData['first_name']) < 1 or len(postData['last_name']) < 1:
            error.append("All fields must be filled")
        try:
            validate_email(postData['email'])
        except ValidationError as e:
            error.append("Email must be a valid email.")
        if len(postData['email']) < 6:
            error.append("Email must be more than 6 characters long.")
        # if User.objects.filter(email__iexact=postData['email']).exclude(user.email):
        #     error.append('Email is already registered.')
        if not postData['first_name'].isalpha():
            error.append("First name cannnot contain numbers or special characters. ")
        if len(postData['first_name']) < 2:
            error.append("First name must be more than 2 characters.")
        if len(postData['last_name']) < 2:
            error.append("Last name must be more than 2 characters.")
        return error

    
    def adminPassVal(self, postData):
        error = []
        if len(postData['password']) < 8:
            error.append("Password must be 8 characters long.")
        if postData['password'] != postData['confirmation_password']:
            error.append("Password and confirmation password don't match.")
        return error

    def adminPassEdit(self, postData, user):
        user = User.objects.get(id=user.id)
        hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        user.password = hashed_pw
        user.save()
        return user

    
    def adminInfoEdit(self, postData, user):
        user = User.objects.get(id=user.id)
        user.email = postData['email']
        user.first_name = postData['first_name']
        user.last_name = postData['last_name']
        user.admin = postData['admin']
        user.save()
        return user


    def removeVal(self, curr_user):
        curr_user=User.objects.get(id=curr_user.id)
        error=[]
        if not curr_user.admin == 'Admin':
            error.append("You don't have authorization to remove users." )
        return error


    def remove(self, user):
        user=User.objects.get(id=user.id)
        user.delete()
        return user
        

class MessageManager(models.Manager):
    def valMessage(self, postData):
        error = []
        if len(postData['content']) < 1:
            error.append("You didn't write a message to send!")
            return error

    def addMessage(self, postData, curr_user, message_to):
        if len(postData['content']) > 0:
            add_message = Message.objects.create(content = postData['content'], user=curr_user, recipient=message_to)
            return add_message
    

class CommentManager(models.Manager):
    def valComment(self, postData):
        error = []
        if len(postData['content']) < 1:
            error.append["You didn't write a comment to send!"]
            return error
    def addComment(self, postData, sender, message_id):
        if len(postData['content']) > 0:
            add_comment = Comment.objects.create(content = postData['content'], user = sender, reply = message_id)
            return add_comment
            

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
    objects = MessageManager()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __repr__(self):
        return '<Message: {} and the {}.>'.format(self.content, self.user) 

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name = "replied_by")
    reply = models.ForeignKey(Message, related_name = "message")
    objects = CommentManager()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __repr__(self):
        return '<Comment: {} said {}'.format(self.user, self.content)
