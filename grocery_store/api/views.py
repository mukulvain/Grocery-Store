from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import DjangoModelPermissions
from .models import *
from .serializers import *


class CorrectedDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }


class Registration_View(generics.CreateAPIView):
    permission_classes = [CorrectedDjangoModelPermissions]
    # authentication_classes = [TokenAuthentication]
    queryset = User.objects.all()
    serializer_class = Registration_Serializer


class Item_Viewset(viewsets.ModelViewSet):
    permission_classes = [CorrectedDjangoModelPermissions]
    # authentication_classes = [TokenAuthentication]
    serializer_class = Item_Serializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("name",)

    def get_queryset(self):
        return Item.objects.all()
