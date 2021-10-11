from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from .models import Bill_Item, Item, Bill


@receiver(pre_save, sender=Bill_Item)
def create_bill_item(sender, instance, **kwargs):
    item = Item.objects.filter(name=instance.item).first()
    if instance._state.adding:
        item.quantity -= instance.quantity
        item.save()
    else:
        item.quantity += (
            Bill_Item.objects.filter(bill_no=instance.bill_no, item=instance.item)
            .first()
            .quantity
        )
        item.save()
        bill = Bill.objects.filter(bill_no=instance.bill_no).first()
        bill.total_price -= (
            Bill_Item.objects.filter(bill_no=instance.bill_no, item=instance.item)
            .first()
            .price
        )
        bill.save()


@receiver(post_save, sender=Bill_Item)
def update_bill_item(sender, instance, created, **kwargs):
    bill = Bill.objects.filter(bill_no=instance.bill_no).first()
    bill.total_price += instance.price
    bill.save()

    if not created:
        item = Item.objects.filter(name=instance.item).first()
        item.quantity -= instance.quantity
        item.save()


@receiver(pre_delete, sender=Bill_Item)
def delete_bill_item(sender, instance, **kwargs):
    bill = Bill.objects.filter(bill_no=instance.bill_no).first()
    bill.total_price -= instance.price
    bill.save()
    item = Item.objects.filter(name=instance.item).first()
    item.quantity += instance.quantity
    item.save()
