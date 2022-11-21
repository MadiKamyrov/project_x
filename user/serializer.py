from django.contrib.auth import authenticate
from rest_framework import serializers

from user.models import User
from django.utils.translation import gettext_lazy as _


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            is_admin=True
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(
        label=_("Password"),
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        password = attrs.get('password')
        email = attrs.get('email')

        if not (email and password):
            msg = _('Must include "password" and "email" or "phone_number".')
            raise serializers.ValidationError(msg, code='authorization')

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )
        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']
