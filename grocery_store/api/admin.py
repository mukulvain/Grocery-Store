from django.contrib import admin
from .models import *

# Register your models here.


class Bill_Item_Inline(admin.StackedInline):
    model = Bill_Item


class Item_Admin(admin.ModelAdmin):
    model = Item
    ordering = ("name",)
    search_fields = ("name",)
    list_display = ("name", "category", "price", "quantity")
    list_filter = ("category",)
    filter_horizontal = ()
    fieldsets = ((None, {"fields": ("name", "category", "price", "quantity")}),)


class Account_Admin(admin.ModelAdmin):
    model = Account
    ordering = ("name",)
    search_fields = ("name", "mobile_no")
    list_display = ("name", "mobile_no")
    list_filter = ()
    filter_horizontal = ()
    fieldsets = ((None, {"fields": ("name", "mobile_no")}),)


class Bill_Admin(admin.ModelAdmin):
    model = Bill
    ordering = ("-date_time",)
    search_fields = ("bill_no", "name_id__name")
    list_display = ("bill_no", "name", "date_time")
    list_filter = ()
    filter_horizontal = ()
    readonly_fields = ("date_time",)
    fieldsets = ((None, {"fields": ("bill_no", "name", "date_time")}),)

    inlines = [Bill_Item_Inline]


class Bill_Item_Admin(admin.ModelAdmin):
    model = Bill
    ordering = ("-bill_no",)
    search_fields = ("bill_no_id__bill_no", "item_id__name")
    list_display = (
        "bill_no",
        "item",
        "quantity",
        "price",
    )
    list_filter = ("item",)
    filter_horizontal = ()
    readonly_fields = ("price",)
    fieldsets = (
        (
            None,
            {"fields": ("bill_no", "item", "quantity", "price")},
        ),
    )


admin.site.register(Bill, Bill_Admin)
admin.site.register(Item, Item_Admin)
admin.site.register(Account, Account_Admin)
admin.site.register(Bill_Item, Bill_Item_Admin)
