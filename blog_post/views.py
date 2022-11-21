from django.shortcuts import render, get_object_or_404
import knox.auth
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from blog_post.models import Post
from blog_post.serializers import PostSerializer
from user.models import User


# Create your views here.

class BlogPostViewSet(viewsets.ViewSet):
    authentication_classes = (knox.auth.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    @action(["post",], detail=True)
    def create_post(self, request):
        try:
            user = get_object_or_404(User, id=request.user.id)
        except Exception:
            return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = Post(title=serializer.validated_data.get("title"), publisher=user)
            post.save()
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(["get",], detail=True)
    def get_posts(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(["post",], detail=True)
    def like_post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Exception:
            return Response({"error": "Post does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        for item in post.like.all():
            if item == request.user:
                return Response({"error": "You already unliked this post"}, status=status.HTTP_400_BAD_REQUEST)
        post.like.add(request.user)
        post.like_count += 1
        for item in post.unlike.all():
            if item == request.user:
                post.unlike.remove(item)
                post.unlike_count -= 1
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(["post",], detail=True)
    def unlike_post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Exception:
            return Response({"error": "Post does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        for item in post.unlike.all():
            if item == request.user:
                return Response({"error": "You already unliked this post"}, status=status.HTTP_400_BAD_REQUEST)
        post.unlike.add(request.user)
        post.unlike_count += 1
        for item in post.like.all():
            if item == request.user:
                post.like.remove(request.user)
                post.like_count -= 1
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)