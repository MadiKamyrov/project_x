from django.contrib.auth import login

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions,viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from user.models import User
from user.serializer import LoginSerializer, RegisterSerializer, UserSerializer


class LoginTokenAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            login(request, user)
            return super(LoginTokenAPI, self).post(request, format=None)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'})


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        _, token = AuthToken.objects.create(user)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        })


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = User.objects.get(id=request.user.id)
        serializer = UserSerializer(instance, context={"request": request})
        return Response(serializer.data)

    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)