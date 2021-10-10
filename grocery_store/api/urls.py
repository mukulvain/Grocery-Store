from rest_framework.authtoken.views import obtain_auth_token
from django.db import router
from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"item", Item_Viewset, "item")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", obtain_auth_token),
    path("register/", Registration_View.as_view()),
]
