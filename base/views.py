from django.shortcuts import render, redirect
from .models import Post, Topic, Message
from .forms import PostForm, MessageForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def loginPage(req):
    page = 'login'
    if req.user.is_authenticated:
        return redirect('home')

    if req.method == 'POST':
        username = req.POST.get('username').lower()
        password = req.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(req, "user doesn exist")

        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)
            return redirect('home')
        else:
            messages.error(req, "login error")

    context = {
        'page':page,
    }
    return render(req, 'base/login_register.html', context)


def logoutUser(req):
    logout(req)
    return redirect('home')


def registerPage(req):
    form = UserCreationForm()
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(req, user)
            return redirect('home')
        else:
            messages.error(req, 'Error occured during registration...')
    return render(req, 'base/login_register.html',{'form':form})


def landpage(req):
    return render(req, 'base/landpage.html')


def home(req):
    q = req.GET.get('q') if req.GET.get('q') != None else ''
    posts = Post.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()[0:5]
    pmessages = Message.objects.filter(Q(post__topic__name__icontains=q))[0:6]
    post_count =  posts.count()
    paginator = Paginator(posts, 3)  # 3 posts in each page
    page = req.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'topics': topics,
        'page': page,
        'post_count': post_count,
        'pmessages': pmessages,
    }
    return render(req, 'home.html', context)


def post(req, pk):
    post = Post.objects.get(id=pk)
    topics = Topic.objects.all()
    pmessages = post.message_set.all().order_by('-created')
    participants = post.participants.all()

    if req.method == 'POST':
        message = Message.objects.create(
            user=req.user, post=post, body = req.POST.get('body')
        )
        # post.participants.add(req.user)
        return redirect('post', pk=post.id)
    context = {
        'post': post,
        'pmessages':pmessages,
        'topics':topics,
        'participants':participants,
            }
    return render(req, 'base/post.html', context)


def userProfile(req, pk):
    user = User.objects.get(id=pk)
    posts = user.post_set.all()
    pmessages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'posts':posts, 'topics':topics, 'pmessages':pmessages}
    return render(req, 'base/profile.html', context)


@login_required(login_url='login')
def createPost(req):
    form = PostForm()
    if req.method == 'POST':
        form = PostForm(req.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = req.user
            post.save()
            return redirect('home')
    context = { 'form': form }
    return render(req, 'base/post_form.html', context)


@login_required(login_url='login')
def updatePost(req, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)

    if req.user != post.user:
        return HttpResponse('u r not allowed...')
    if req.method == 'POST':
        form = PostForm(req.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = { 'form': form }
    return render(req, 'base/post_form.html', context)


@login_required(login_url='login')
def deletePost(req, pk):
    post = Post.objects.get(id=pk)

    if req.user != post.user:
        return HttpResponse('u r not allowed...')
    if req.method == 'POST':
        post.delete()
        return redirect('home')
    return render(req, 'base/delete.html', {'obj':post})


@login_required(login_url='login')
def deleteMessage(req, pk):
    message = Message.objects.get(id=pk)

    if req.user != message.user:
        return HttpResponse('u r not allowed...')
    if req.method == 'POST':
        message.delete()
        return redirect('home')
    return render(req, 'base/delete.html', {'obj':message})


def topicsPage(req):
    q = req.GET.get('q') if req.GET.get('q') != None else ''
    topics = Topic.objects.filter(Q(name__icontains=q))
    return render(req,'base/topics.html', {'topics': topics})


def activityPage(req):
    pmessages = Message.objects.all()
    return render(req,'base/activity.html', {'pmessages': pmessages})