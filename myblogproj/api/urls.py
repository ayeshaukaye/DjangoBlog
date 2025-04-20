from django.urls import path
from .views import PostListCreateAPIView, PostDetailAPIView, CommentListCreateAPIView,CategoryListAPIView

urlpatterns = [
    path('api/posts', PostListCreateAPIView.as_view(), name='APIPostList'),
    path('api/posts/<int:pk>', PostDetailAPIView.as_view(), name='APIPostDetail'),
    path('api/<int:pk>/comments/', CommentListCreateAPIView.as_view(), name='APICommentList'),
    path('api/categories', CategoryListAPIView.as_view(), name='APICategoryList'),
    

]