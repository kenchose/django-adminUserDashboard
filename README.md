# Cockpit - Admin user dashboard

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Prerequisites](#prerequisites)
* [Setup](#setup)

## General info
Full authorization for CRUD operations to admin users. Only the user can edit their profile while others cannot if not an admin user. Any user can post and reply to any messages on each others profile page. Validations and authenticity are implemented when creating a user, during login, editing, and posting messages.

## Technologies
* Bcrypt version:3.1.4
* Python version: 2.7.10
* MySQL version: 14.14
* Django version: 1.10
* Bootstrap version: 4.3.1

## Prerequisites

What things you need to install the software and how to install them
```
$ brew update
$ brew install python
$ pip install
Mac/Linux: $ pip install virtualenv
Windows: $ python -m install virtualenv
$ virtualenv djangoEnv
```
## Setup
* Clone this repo to your local machine using `https://github.com/kenchose/django-adminUserDashboard.git`
To run this project, install it locally using pip:
```
$ ../djangoEnv
$ source djangoEnv/bin/activate
$ pip install Django==1.10
$ pip install bcrypt
```
* Go to the root of the project and run python manage.py runserver
* To login as an admin user:
  - email: kenny@pham.com
  - password: password

# Enjoy!
