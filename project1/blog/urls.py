from django.urls import path
from .views import (HomeView,PostListView, PostDetailView, 
                    CreatePostView, PostUpdateView, PostDeleteView,
                    DraftListView, add_comments_to_post, comment_approve,comment_remove,post_publish)

urlpatterns = [
    path("", PostListView.as_view(), name="post_list" ),
    path("home/", HomeView.as_view(),name="home"),
    path("post/<int:pk>/", PostDetailView.as_view(), name='post_detail'),
    path("post/create/", CreatePostView.as_view(), name='post_create'),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name='post_edit'),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name='post_remove'),
    path("drafts/", DraftListView.as_view(), name='draft_list'),
    path("post/<int:pk>/comment/", add_comments_to_post, name='add_comment_to_post' ),
    path("comment/<int:pk>/approve/", comment_approve, name='comment_approve' ),
    path("comment/<int:pk>/remove/", comment_remove, name='comment_remove' ),
    path("post/<int:pk>/publish/", post_publish, name='post_publish' ),
    
]