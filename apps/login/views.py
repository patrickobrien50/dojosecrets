from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count

from .models import User, Post

# Create your views here.

def index(request):
    return render(request, 'login/index.html')

def register(request):
    user = User.objects.validateRegister(request.POST)
    if user[0] == False:
        for error in user[1]:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['id'] = user[1].id
        print "Welcome User", request.session['id']
        context = {
        'users': User.objects.get(email=request.POST['email'])
        }
        return redirect("/success")

def login(request):
    user = User.objects.loginValidate(request.POST)
    if user[0] == False:
        for error in user[1]:
            messages.error(request, error)
        return redirect('/')
    else:
        print "We made it"
        if 'id' not in request.session:
            request.session['id'] = user[1].id
        print "got session", request.session['id']
        context = {
        'users': User.objects.get(email=request.POST['email'])
        }
        return redirect("/success")

def success(request):
    user = User.objects.get(id=request.session['id'])
    context = {
    'users': user,
    # 'posts': Post.objects.all(),
    'posts': Post.objects.annotate(num_likes=Count('likes'))
    }
    return render(request, 'login/home_page.html', context)

def makePost(request):
    post = Post.objects.postValidate(request.POST['post'], request.session['id'])
    if post[0] == False:
        for error in post[1]:
            messages.error(request, error)
        return redirect("/success")
    else:
        print Post.objects.all()
        return redirect("/success")

def likePost(request):
    post = Post.objects.likePost(request.POST, request.session['id'])
    return redirect("/success")

def mostLikes(request):
    return render(request, 'login/most_liked.html', {'posts': Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')})

def deletePost(request):
    Post.objects.get(id=request.POST['deleteid']).delete()
    return redirect("/success")


def logout(request):
    request.session.pop('id')
    return render(request, 'login/index.html')
