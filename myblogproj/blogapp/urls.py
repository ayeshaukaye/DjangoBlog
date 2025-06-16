from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path("", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("category/<category>/", views.blog_category, name="blog_category"),
    path("register/", views.blog_register, name="blog_register"),
    path("about/",views.blog_about, name="blog_about"),
    path("login/",views.blog_login, name="blog_login"), 
    path("search/",views.blog_search, name="blog_search"), 
    path("logout/",views.blog_logout, name="blog_logout"), 
    path("exclusive/",views.blog_exclusive, name="blog_exclusive"), 
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path("for you/",views.blog_recommend, name="blog_recommend"), 


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


