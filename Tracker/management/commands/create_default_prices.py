from django.core.management.base import BaseCommand, CommandError

from Tracker.models import Item, Price

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        prices = [0, 4.99, 5.99, 6.99, 7.99, 8.99, 9.99, 10.99, 11.99, 12.99, 13.99, 14.99, 19.99, 24.99, 29.99, 34.99, 39.99, 44.99, 49.99, 54.99, 59.99, 64.99, 69.99, 74.99, 79.99, 84.99, 89.99, 94.99, 99.99, 109.99, 119.99, 129.99, 139.99, 149.99, 159.99, 169.99, 179.99, 189.99, 199.99, 209.99, 219.99, 229.99, 239.99, 249.99, 299.99, 349.99, 399.99, 449.99, 499.99, 599.99, 699.99, 799.99, 899.99, 999.99, 1099.99, 1199.99, 1299.99, 1399.99, 1499.99]

        for price in prices:
            obj = Price(amount=price)
            obj.save()
