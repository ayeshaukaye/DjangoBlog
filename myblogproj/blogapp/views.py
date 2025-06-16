from email.policy import default
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from blogapp.models import Post, Comment, PostView
from blogapp.forms import CommentForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from collections import defaultdict

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

@login_required(login_url="/login/")
def blog_recommend(request):
    user = request.user

    liked_ids = set(user.post_likes.values_list('id', flat=True))
    viewed_ids = set(PostView.objects.filter(user=user).values_list('post_id', flat=True))
    interacted_ids = liked_ids.union(viewed_ids)

    # print(interacted_ids)

    user_posts = Post.objects.filter(id__in = interacted_ids)
    user_cat_id = set(user_posts.values_list('categories__id', flat=True))
    user_tag_id = set(user_posts.values_list('tags__id', flat=True))
    
    candidate_posts = Post.objects.exclude(id__in=interacted_ids)

    scoredposts = defaultdict(int)

    for post in candidate_posts.prefetch_related('categories', 'tags','likes'):
        score = 0

        # matching category
        match_cat_id = set(post.categories.values_list('id', flat=True))
        score += 2 * len(user_cat_id.intersection(match_cat_id))

        # matching tag
        match_tag_id = set(post.tags.values_list('id', flat=True))
        score += 3 * len(user_tag_id.intersection(match_tag_id))

        # liked by user who liked same post
        match_like = post.likes.filter(
            post_likes__in=liked_ids
        ).distinct().count()
        score += match_like * 1

        # viewed by user who viewed same post
        match_view = PostView.objects.filter(
            post = post,
            user__postview__post_id__in=viewed_ids
        ).values('user').distinct().count()
        score += match_view * 0.5

        if score > 0:
            scoredposts[post] = score

    recommended = sorted(scoredposts.items(), key=lambda x: x[1], reverse=True)
    top_posts = [post for post, score in recommended[:4]]

    context = {
            "posts": top_posts
        }

    return render(request, 'blogapp/for you.html', context)



