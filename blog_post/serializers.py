from blog_post.models import Post
from rest_framework import serializers

from user.serializer import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    like = UserSerializer(many=True, read_only=True)
    unlike = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'publisher', 'like_count', 'unlike_count','like', 'unlike']
        read_only_fields = ['id', 'publisher',]


class PostSerializerLike(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'like', 'publisher', ]
        read_only_fields = ['id', 'publisher']


class PostSerializerUnlike(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'unlike', 'publisher', ]
        read_only_fields = ['id', 'publisher']
