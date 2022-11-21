from django.urls import path
from knox import views as knox_views
from rest_framework import routers

from user.views import LoginTokenAPI, RegisterAPI, UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)


urlpatterns = router.urls
urlpatterns += [
    path('register/', RegisterAPI.as_view(), name="register"),
    path('login/', LoginTokenAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]