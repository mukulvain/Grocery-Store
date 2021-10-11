from rest_framework.authtoken.views import obtain_auth_token
from django.db import router
from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"item", Item_Viewset, "item")
router.register(r"account", Account_Viewset, "item")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", obtain_auth_token),
    path("register/", Registration_View.as_view()),
    path("staff/", Staff_View.as_view()),
    path("bill/", bill),
    path("bill/<str:bill_no>", bill_specific),
    path("customer_bill/<str:mobile_no>", customer_bill),
]
