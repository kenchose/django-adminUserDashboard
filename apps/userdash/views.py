# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.messages import get_messages
from datetime import datetime
from . models import *


def index(request):
    return render(request, 'userdash/index.html')


def signin(request):
    return render(request, 'userdash/signin.html')


def registration(request):
    return render(request, "userdash/registration.html")


def register(request):
    if request.method == "POST":
        result = User.objects.register(request.POST)
        if len(result) > 0:
            for error in result:
                messages.error(request, error)
            return redirect ('/registration')
        else:
            newUser = User.objects.newUser(request.POST)
            request.session['id'] = newUser.id
            if newUser.id == 1:
                # newUser.admin == "Admin" Code already exixsts within models newUser method
                # newUser.save()
                return redirect('/dashboard/admin')
            else:
                return redirect('/dashboard')
    else:
        return redirect ('/registration')


def login(request):
    if request.method == "POST":
        result = User.objects.loginValid(request.POST)
        try: 
            if len(result) > 0:
                for error in result:
                    messages.error(request, error)
                    return redirect ('/signin')
        except:
            retrieved_user = User.objects.loginUser(request.POST)
            request.session['id'] = retrieved_user.id
            if retrieved_user.id == 1:
                return redirect ('/dashboard/admin')
            else:
                return redirect ('/dashboard')
    else:
        return redirect('/signin')
    


def dashboard(request):
    if 'id' in request.session:
        user = User.objects.get(id=request.session['id'])
        all_users = User.objects.all()
        context = {
            "curr_user": user,
            "all_users": all_users,
        }
        return render (request, 'userdash/dashboard.html', context)
    else: 
        return redirect('/')

def admindash(request):
    if 'id' in request.session:
        user = User.objects.get(id=request.session['id'])
        all_users = User.objects.all()
        context = {
            "curr_user": user,
            "all_users": all_users,
        }
        return render (request, 'userdash/admindash.html', context) #corrected the path of admin path template
    else: 
        return redirect('/signin')

def userProfile(request, user_id):
    users = User.objects.get(id=user_id)
    curr_user = User.objects.get(id=request.session['id'])
    msg = Message.objects.filter(recipient=user_id).order_by("-created_at")
    context = {
        "users": users,
        "curr_user": curr_user,
        "msg": msg,
    }
    return render (request, "userdash/profile.html", context)

def messageFor(request, user_id):
    if request.method == "POST":
        sender = User.objects.get(id=request.session['id'])
        recipient = User.objects.get(id=user_id)
        message = Message.objects.valMessage(request.POST)
        try:
            if len(message) > 0:
                for error in message:
                    messages.error(request, error)
                    return redirect ("/users/show/{}".format(user_id))
        except:
            add_message = Message.objects.addMessage(request.POST, sender, recipient)
            print (add_message.__dict__)
            return redirect ("/users/show/{}".format(user_id))
    else:
        return redirect ("/users/show/user_id")


def commentTo(request, user_id, msg_id):
    if request.method == "POST":
        commenter = User.objects.get(id=request.session['id'])
        message = Message.objects.get(id=msg_id)
        recipient = User.objects.get(id=user_id)
        comment = Comment.objects.valComment(request.POST)
        try:
            if len(comment) > 0:
                for error in comment:
                    messages.error(request, error)
                    return redirect ("/users/show/{}".format(user_id))
        except:
            new_comment = Comment.objects.addComment(request.POST, commenter, message)
            return redirect ("/users/show/{}".format(user_id))
    else:
        return redirect ("/users/show/{}".format(user_id))


def userEdit(request, user_id):
    users = User.objects.get(id=user_id)
    error = []
    if request.session['id'] != users.id:
        error.append("You cannot edit other user's profile information.") 
    if error:
        for error in error:
            messages.error(request, error)
            return redirect ("/users/show/{}".format(user_id))
    context = {
        "users": users,
    }
    return render (request, "userdash/user_edit.html", context)


def userEditInfo(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        new_info = User.objects.editInfoVal(request.POST, user)
        # try:
        if len(new_info) > 0:
            for error in new_info:
                messages.error(request, error)
                return redirect ('/edit/{}'.format(user_id))
        # except:
        else:
            update_info = User.objects.editInfo(request.POST, user)
            messages.success(request, "Your information have been successfully updated.")
            return redirect ('/users/show/{}'.format(user_id))
    else:
        return redirect('/users/show/{}'.format(user_id))
        



















def usersEdit(request):
    user = User.objects.get(id=id)
    context = {
        "curr_user": user
    }
    return render (request, "/userdash/profile.html")




def logout(request):
    request.session.clear()
    return redirect('/')