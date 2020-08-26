from django.urls import path
from . import views

app_name="blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("article/search/", views.search, name="search"),
    path("register/", views.sign_in, name="register"),
    path("login/", views.login, name="login"),
    path("article/<str:str>/", views.show_post, name="show_post")
]
