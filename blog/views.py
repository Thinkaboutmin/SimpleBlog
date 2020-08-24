from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as log, logout as logo
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.http.response import HttpResponseBadRequest
from .forms import SigninForm, LoginForm, CommentForm
from .models import Post
from datetime import datetime

@require_GET
def index(request):
    posts = Post.objects.order_by("-pub_date")

    return render(request, "base.html", {"posts": posts})

@require_GET
def search(request):
    posts = Post.objects.filter(header__contains=request.GET["header"])

    return render(request, "base.html", {"posts": posts})

@require_http_methods(["GET", "POST"])
def show_post(request, str):
    """
    Show the post content when the request is a GET. If a POST is given,
    it will try to save a comment for the POST, according to the values passed.

    @param request The request from the client.
    @param str The post header.

    The return will always be the template file "detail.html".
    """

    # It's guaranteed to always have a unique header.
    post = get_object_or_404(Post, header=str)

    comments = post.comment_set.order_by("-comment_date")
    # Save a comment to given post.
    if (request.method == "POST"):
        # Because we add a few things at the comment creation,
        # we pass it with the data argument.
        comment_form = CommentForm(data={
            "post": post,
            "comment_date": datetime.now(),
            "author": request.user,
            "content": request.POST["content"],
        })

        if (comment_form.is_valid()):
            comment_form.save()
            comment_form = CommentForm()
    else :
        comment_form = CommentForm()

    return render(request, "detail.html", {
        "post": post,
        "comment_form": comment_form,
        "comments": comments
    })

@require_http_methods(["GET", "POST"])
def sign_in(request):
    if (request.method == "POST"):
        form = SigninForm(request.POST)
        if (form.is_valid()):
            form.save()
            loginForm = LoginForm(data={
                "password": request.POST["password1"],
                "username": request.POST["username"]
            })

            if (loginForm.is_valid()):
                log(request, loginForm.user_cache)

            redirect_url = request.POST.get("redirect", "index")
            return redirect(redirect_url)
        
    else:
        form = SigninForm()

    url_redirect = request.GET.get("redirect", "index")
    return render(request, "register.html", {"form": form, "url_redirect": url_redirect})

@require_http_methods(["GET", "POST"])
def login(request):
    if (request.method == "POST"):
        form = LoginForm(data=request.POST)
        if (form.is_valid()):
            log(request, form.user_cache)

            url_redirect = request.POST.get("redirect", "index")
            
            return redirect(url_redirect)
    
    form = LoginForm()
    url_redirect = request.GET.get("redirect", "index")

    return render(request, "login.html", {"form": form, "url_redirect": url_redirect})
    
@require_http_methods(["GET", "POST"])
def make_post(request):

    return None

@require_GET
def which_user(request):
    return render(request, "which_user.html", {"user": request.user})

def logout(request):
    if (request.user.is_authenticated):
        logo(request)

        return redirect("login")
    
    return HttpResponseBadRequest("Can't logout if no user is logged or authenticated.")
