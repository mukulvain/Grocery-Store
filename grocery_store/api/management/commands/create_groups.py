from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


def Owner():
    owner, created = Group.objects.get_or_create(name="Owner")
    owner.permissions.add(Permission.objects.get(codename="add_account"))
    owner.permissions.add(Permission.objects.get(codename="change_account"))
    owner.permissions.add(Permission.objects.get(codename="delete_account"))
    owner.permissions.add(Permission.objects.get(codename="view_account"))
    owner.permissions.add(Permission.objects.get(codename="add_bill"))
    owner.permissions.add(Permission.objects.get(codename="change_bill"))
    owner.permissions.add(Permission.objects.get(codename="view_bill"))
    owner.permissions.add(Permission.objects.get(codename="add_bill_item"))
    owner.permissions.add(Permission.objects.get(codename="change_bill_item"))
    owner.permissions.add(Permission.objects.get(codename="delete_bill_item"))
    owner.permissions.add(Permission.objects.get(codename="view_bill_item"))
    owner.permissions.add(Permission.objects.get(codename="add_item"))
    owner.permissions.add(Permission.objects.get(codename="change_item"))
    owner.permissions.add(Permission.objects.get(codename="view_item"))
    owner.permissions.add(Permission.objects.get(codename="delete_item"))
    # Ideally item should not be deleted rather its quantity should be dropped to zero.
    # But since its written in the question, therefore I am allowing the owner to delete the item


def Cashier():
    cashier, created = Group.objects.get_or_create(name="Cashier")
    cashier.permissions.add(Permission.objects.get(codename="add_account"))
    cashier.permissions.add(Permission.objects.get(codename="change_account"))
    cashier.permissions.add(Permission.objects.get(codename="view_account"))
    cashier.permissions.add(Permission.objects.get(codename="add_bill"))
    cashier.permissions.add(Permission.objects.get(codename="change_bill"))
    cashier.permissions.add(Permission.objects.get(codename="view_bill"))
    cashier.permissions.add(Permission.objects.get(codename="add_bill_item"))
    cashier.permissions.add(Permission.objects.get(codename="change_bill_item"))
    cashier.permissions.add(Permission.objects.get(codename="delete_bill_item"))
    cashier.permissions.add(Permission.objects.get(codename="view_bill_item"))


def Inventory_Admin():
    inventory_admin, created = Group.objects.get_or_create(name="Inventory_Admin")
    inventory_admin.permissions.add(Permission.objects.get(codename="add_item"))
    inventory_admin.permissions.add(Permission.objects.get(codename="change_item"))
    inventory_admin.permissions.add(Permission.objects.get(codename="view_item"))


class Command(BaseCommand):
    help = "This command is used to generate monthly maintenance bills"

    def handle(self, *args, **options):
        Owner()
        Cashier()
        Inventory_Admin()
        self.stdout.write("Groups created successfully.")
