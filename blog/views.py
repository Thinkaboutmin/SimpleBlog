from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as log, logout as logo
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.http.response import HttpResponseBadRequest, Http404
from .forms import SigninForm, LoginForm, CommentForm
from .models import Post
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage

@require_GET
def index(request):
    """
    Show the main page with all the posts.

    The index uses pagination, 5 posts per page.

    @param request The request from the client.

    Return the base.html page if the page exists otherwise returns 400 error page.
    """
    tmp_posts = Post.objects.order_by("-pub_date")
    posts_page = Paginator(tmp_posts, 5)
    # Default to page one when none is given
    page = request.GET.get("page", 1)
    try:
        posts = posts_page.page(page)
    except EmptyPage:
        return render(
            request,
            "error.html",
            {
                "message": f"Could not find page: {page}",
                "title_text": "Page not found - Post"
            },
            status=400
        )
    
    return render(
        request,
        "base.html", 
        {
        "posts": posts,
        }
    )

@require_GET
def search(request):
    """
    Search for posts according to what was given.
    The search will be based if the header contains some or all
    the text of what was given.

    The search uses pagination, 5 Posts per page. If the given
    page parameter returns an EmptyPage exception an error page will
    be given.

    @param request The request from the client.

    Return the base.html page if the page exists otherwise returns 400 error page.
    """
    tmp_posts = Post.objects.order_by("-pub_date").filter(header__contains=request.GET["header"])
    posts_page = Paginator(tmp_posts, 5)
    # Default to page one when none is given
    page = request.GET.get("page", 1)
    try:
        posts = posts_page.page(page)
    except EmptyPage:
        return render(
            request,
            "error.html",
            {
                "message": f"Could not find page: {page}",
                "title_text": "Page not found - Post"
            },
            status=400
        )

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
    """
    Sign in users to the blog. If the request is a
    GET it will return the registration form. If it's
    a POST, it will register the user to the database
    according to what was given in the request.

    @param request The request from the client.

    Returns a page form if it's a GET otherwise redirects if it's a POST.
    """
    if (request.method == "POST"):
        form = SigninForm(request.POST)
        if (form.is_valid()):
            form.save()
            loginForm = LoginForm(data={
                "password": request.POST["password1"],
                "username": request.POST["username"]
            })

            if (loginForm.is_valid()):
                # Well, the user registered
                # so, let's login it already as well.
                log(request, loginForm.user_cache)

            # Redirect the user to it's last page.
            redirect_url = request.POST.get("redirect", "index")
            return redirect(redirect_url)
        
    else:
        form = SigninForm()

    # Put the redirect value to index, just to be sure.
    url_redirect = request.GET.get("redirect", "index")
    return render(request, "register.html", {"form": form, "url_redirect": url_redirect})

@require_http_methods(["GET", "POST"])
def login(request):
    """
    Returns a login form for the user if the request is a GET. If
    it's a POST, it log in the user and redirect to the last page.

    @param request The request from the client.

    Return a login form if it's a GET otherwise redirects to the last page if it's POST
    """
    if (request.method == "POST"):
        form = LoginForm(data=request.POST)
        if (form.is_valid()):
            # Whenever the LoginForm.is_valid is ran it will
            # generate a variable with an User object called user_cache. We
            # just pick it and log it as it haves the same data to what was given.
            log(request, form.user_cache)

            url_redirect = request.POST.get("redirect", "index")
            
            return redirect(url_redirect)
    
    form = LoginForm()
    # Put the redirect value to index, just to be sure.
    url_redirect = request.GET.get("redirect", "index")

    return render(request, "login.html", {"form": form, "url_redirect": url_redirect})