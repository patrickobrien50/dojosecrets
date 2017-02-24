from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

Email_Regex = re.compile (r'^[a-zA-Z0-9.+_]+@[a-zA-Z0-9._-]+[a-zA-Z]+$')
Name_Regex = re.compile (r'^[a-zA-Z]+$')
Post_Regex = re.compile (r'^[^\s].+$')

class LoginManager(models.Manager):
    def validateRegister(self, postData):
        status = True
        errorlist = []
        if not Name_Regex.match(postData['first_name']):
            errorlist.append("Must provide valid first name!")
            status = False
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errorlist.append("Name must have at least 2 letters!")
            status = False
        if not Name_Regex.match(postData['last_name']):
            errorlist.append("Must provide valid last name!")
            status = False
        if not Email_Regex.match(postData['email']):
            errorlist.append("Must provide a valid email!")
            status = False
        if len(postData['password']) < 8:
            errorlist.append("Password must be at least 8 characters!")
            status = False
        if postData['password'] != postData['confirm']:
            errorlist.append("Passwords must match!")
            status = False
        if len(User.objects.filter(email=postData['email'])) > 0:
            errorlist.append("Email is already registered!")
            status = False
        if status == False:
            return (False, errorlist)
        else:
            password = postData['password']
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            newuser = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=hashed)
            return (True, newuser)

    def loginValidate(self, postData):
        olduser = User.objects.filter(email=postData['email'])
        status = True
        errorlist = []
        if len(olduser) < 1:
            errorlist.append("Must register!")
            status = False
        if len(postData['email']) < 1:
            errorlist.append("Must provide a valid email!")
            status = False
        if len(postData['password']) < 1:
            errorlist.append("Must provide a valid password")
            status = False
        if status == False:
            return (False, errorlist)
        else:
            if bcrypt.hashpw(postData['password'].encode(), olduser[0].password.encode()) == olduser[0].password:
                return (True, olduser[0])
            else:
                errorlist.append("Incorrect Password")
                return (False, errorlist)

class PostManager(models.Manager):

    def postValidate(self, post, id):
        status = True
        errorlist = []
        if not Post_Regex.match(post):
            errorlist.append("Post cannot be blank")
            status = False
        if status == False:
            return(False, errorlist)
        else:
            user = User.objects.get(id=id)
            newpost = self.create(description=post, created_by=user)
            return (True, newpost)

    def likePost(self, postData, id):
        user = User.objects.get(id=id)
        post = self.get(id=postData['postid'])
        post.likes.add(user)
        return post



class User(models.Model):
    objects = LoginManager()
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Post(models.Model):
    objects = PostManager()
    created_by = models.ForeignKey(User)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="user_likes")
