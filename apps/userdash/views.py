# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout
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
                # newUser.admin == "Admin" Code already within models newUser method
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
    # if 'id' in request.session:
    user = User.objects.get(id=request.session['id'])
    all_users = User.objects.all()
    context = {
        "curr_user": user,
        "all_users": all_users,
    }
    return render (request, 'userdash/dashboard.html', context)
    # else: 
    #     return redirect('/')

def admindash(request):
    # if 'id' in request.session:
    user = User.objects.get(id=request.session['id'])
    all_users = User.objects.all()
    context = {
        "curr_user": user,
        "all_users": all_users,
    }
    return render (request, 'userdash/admindash.html', context) #corrected the path of admin path template
    # else: 
    #     return redirect('/signin')



#  
def logout(request):
    request.session.clear()
    return redirect('/')