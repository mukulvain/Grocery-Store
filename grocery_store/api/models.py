from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token


class Item(models.Model):
    name = models.CharField(_("Name"), max_length=100, primary_key=True)
    category = models.CharField(_("Category"), max_length=25)
    price = models.IntegerField(_("Price"))
    quantity = models.IntegerField(_("Quantity in Stock"))

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Account(models.Model):
    s_no = models.AutoField(_("Id"), primary_key=True)
    name = models.CharField(_("Name"), max_length=50)
    mobile_no = models.CharField(_("Mobile Number"), max_length=10)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        ordering = ["name"]
        unique_together = ("name", "mobile_no")

    def __str__(self):
        return self.name


class Bill(models.Model):
    bill_no = models.CharField(_("Bill No."), primary_key=True, max_length=15)
    date_time = models.DateTimeField(_("Date and Time"), auto_now_add=True)
    name = models.ForeignKey(
        Account, on_delete=models.CASCADE, verbose_name=_("Customer Name")
    )

    def __str__(self):
        return self.bill_no

    class Meta:
        ordering = ["-date_time"]
        verbose_name = "Bill"
        verbose_name_plural = "Bills"
        unique_together = ("name", "date_time")


class Bill_Item(models.Model):
    s_no = models.AutoField(primary_key=True)
    bill_no = models.ForeignKey(
        Bill, on_delete=models.CASCADE, verbose_name=_("Bill No.")
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name=_("Item"))
    quantity = models.IntegerField(_("Quantity"))
    price = models.IntegerField(_("Price"), editable=False)

    def save(self, *args, **kwargs):
        self.price = self.item.price * self.quantity
        super(Bill_Item, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-bill_no"]
        verbose_name = "Bill Item"
        verbose_name_plural = "Bill Items"
        unique_together = ("bill_no", "item")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
