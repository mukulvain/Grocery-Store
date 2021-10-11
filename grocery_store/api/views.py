from rest_framework import generics, viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import DjangoModelPermissions
from .models import *
from rest_framework.decorators import (
    api_view,
    authentication_classes,
)
from .serializers import *
from rest_framework.response import Response


class CorrectedDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }


class Registration_View(generics.CreateAPIView):
    permission_classes = [CorrectedDjangoModelPermissions]
    authentication_classes = [TokenAuthentication]
    queryset = User.objects.all()
    serializer_class = Registration_Serializer

class Staff_View(generics.ListAPIView):
    permission_classes = [CorrectedDjangoModelPermissions]
    authentication_classes = [TokenAuthentication]
    queryset = User.objects.all()
    serializer_class = User_Serializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("username",)
    
class Item_Viewset(viewsets.ModelViewSet):
    permission_classes = [CorrectedDjangoModelPermissions]
    authentication_classes = [TokenAuthentication]
    serializer_class = Item_Serializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("name","category")

    def get_queryset(self):
        return Item.objects.all()


class Account_Viewset(viewsets.ModelViewSet):
    permission_classes = [CorrectedDjangoModelPermissions]
    authentication_classes = [TokenAuthentication]
    serializer_class = Account_Serializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("mobile_no","name")

    def get_queryset(self):
        return Account.objects.all()


@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
def bill(request):
    if request.method == "GET":
        bills = Bill.objects.all()
        serializer_bill = Bill_Serializer(bills, many=True)
        for i in serializer_bill.data:

            account = Account.objects.filter(mobile_no=i["customer"])[0]
            serializer_account = Account_Serializer(account)
            i["customer"] = serializer_account.data
            bill_items = Bill_Item.objects.filter(bill_no=i["bill_no"])
            serializer_bill_item = Bill_Item_Serializer(bill_items, many=True)
            i["items"] = serializer_bill_item.data
            for j in i["items"]:
                j.pop("bill_no")
        return Response(serializer_bill.data)

    elif request.method == "POST":
        bill = {}
        bill_no = request.data["bill_no"]
        bill["bill_no"] = bill_no
        bill["customer"] = request.data["customer"]["mobile_no"]
        serializer_bill = Bill_Serializer(data=bill)
        if not serializer_bill.is_valid():
            return Response(serializer_bill.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer_bill.save()

        items = request.data["items"]
        for i in items:
            i["bill_no"] = request.data["bill_no"]
        serializer_bill_item = Bill_Item_Serializer(data=items, many=True)
        if not serializer_bill_item.is_valid():
            bill.delete()
            return Response(
                serializer_bill_item.errors, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer_bill_item.save()
            resp = Bill.objects.filter(bill_no=bill_no)[0]
            serialized_resp = Bill_Serializer(resp).data
            return Response(serialized_resp, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT"])
@authentication_classes([TokenAuthentication])
def bill_specific(request, bill_no):
    try:
        Bill.objects.get(bill_no=bill_no)
    except Bill.DoesNotExist:
        return Response("Bill does not exist", status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        bill_items = Bill_Item.objects.filter(bill_no=bill_no)
        serializer_bill_item = Bill_Item_Serializer(bill_items, many=True)
        items = serializer_bill_item.data
        bill = Bill.objects.filter(bill_no=bill_no)[0]
        account = Account.objects.filter(mobile_no=bill.customer.mobile_no).first()
        resp = {}
        resp["items"] = items
        resp["customer"] = Account_Serializer(account).data
        for j in items:
            j.pop("bill_no")
        return Response(resp)

    elif request.method == "PUT":
        bill_items = Bill_Item.objects.filter(bill_no=bill_no)
        bill_items.delete()
        items = request.data["items"]
        for i in items:
            i["bill_no"] = bill_no
        serializer_bill_item = Bill_Item_Serializer(data=items, many=True)
        if not serializer_bill_item.is_valid():
            return Response(
                serializer_bill_item.errors, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer_bill_item.save()
            resp = Bill.objects.filter(bill_no=bill_no)[0]
            serialized_resp = Bill_Serializer(resp).data
            return Response(serialized_resp, status=status.HTTP_202_ACCEPTED)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def customer_bill(request, mobile_no):

    try:
        Account.objects.get(mobile_no=mobile_no)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        bills = Bill.objects.filter(customer=mobile_no)
        serializer_bills = Bill_Serializer(bills, many=True)
        bill_data = serializer_bills.data

        for i in bill_data:
            bill_items = Bill_Item.objects.filter(bill_no=i["bill_no"])
            serializer_bill_items = Bill_Item_Serializer(bill_items, many=True)

            bill_items_data = serializer_bill_items.data
            for j in bill_items_data:
                j.pop("bill_no")
            i["items"] = bill_items_data

        return Response(bill_data)
