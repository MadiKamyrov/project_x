from django.urls import path
from blog_post import views

post_list = views.BlogPostViewSet.as_view({"post": "create_post", "get": "get_posts"})
post_like = views.BlogPostViewSet.as_view({"post": "like_post",})
post_unlike = views.BlogPostViewSet.as_view({"post": "unlike_post"})
urlpatterns = [
    path('post/', post_list, ),
    path('post/<int:pk>/like/',post_like),
    path('post/<int:pk>/unlike/', post_unlike, name="post_unlike"),
]