from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class Account_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class Item_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class Bill_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = "__all__"


class Bill_Item_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Bill_Item
        fields = "__all__"


class Registration_Serializer(serializers.ModelSerializer):

    password1 = serializers.CharField(
        label="Password", style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        label="Confirm Password", style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "groups")

    def save(self):
        staff_account = User(
            username=self.validated_data["username"],
        )
        password1 = self.validated_data["password1"]
        password2 = self.validated_data["password2"]

        if password1 != password2:
            raise serializers.ValidationError({"password": "Passwords should match"})

        staff_account.set_password(password1)
        staff_account.save()
        staff_account.groups.set(self.validated_data["groups"])

        return staff_account

# class User_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username',)