from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from blogapp.models import Post, Comment, PostView
from blogapp.forms import CommentForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts": posts,
    }
    return render(request, "blogapp/index.html", context)

def blog_category(request, category):
    posts = Post.objects.filter(categories__name__contains=category).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blogapp/category.html", context)

def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)
    
    # to track user's viewed posts
    if request.user.is_authenticated:
        PostView.objects.create(user=request.user, post=post) 
    
    comments = Comment.objects.filter(post=post)

    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
    }
    return render(request, "blogapp/detail.html", context)

def blog_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # form.save()
            login(request, form.save()) # form.save() returns user value
            return HttpResponseRedirect(request.path_info)
        else:
            print()
            #form = UserCreationForm()
    else:
        form = UserCreationForm()
    context= {
        "form": form
    }
    return render(request, "blogapp/register.html", context)

def blog_about(request):
    return render(request, "blogapp/about.html")

def blog_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next')) #'next' is name of the hidden input from the form in login.html
            else:
                return HttpResponseRedirect('/')
        else:
            #print(form.errors)
            pass
    else:
        form = AuthenticationForm()
    context = {
        "form":form
    }
    return render(request, "blogapp/login.html", context)

def blog_search(request):   
        query = request.GET.get("query", '')
        if query:
            queryset = Post.objects.filter(
                Q(title__icontains=query) | Q(categories__name__icontains=query) |  Q(tags__name__icontains=query)
            ).distinct()
        else:
            queryset = Post.objects.none()

        context = {
            "posts": queryset
        }
        return render(request, "blogapp/search.html", context)

def blog_logout(request):
    if request.method == "POST":
        logout(request)

    #return render(request, "blogapp/index.html")
    return HttpResponseRedirect('/')

@login_required(login_url="/login/")
def blog_exclusive(request):
    return render(request, "blogapp/exclusive.html")


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('blog_detail', pk=pk)
