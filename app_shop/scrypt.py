import os
from typing import List

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "og_shop.settings")
django.setup()

from app_shop.models import Order, OrderItem
from django.db.models import Count, Sum
from django.db import connection


def get_users_stuff(name: str) -> List:
    global order
    orders_by_userid_total_price = list(
        Order.objects.filter(buyer__username=name).values('id').annotate(prices=Sum('cart__price')))
    prod_ides = list(map(lambda item: item['id'], orders_by_userid_total_price))
    order_by_product = list(
        Order.objects.filter(pk__in=prod_ides).values('cart__product__name', 'cart__quantity', 'id'))

    if orders_by_userid_total_price:
        for order in orders_by_userid_total_price:
            order['products'] = list(filter(lambda item: item['id'] == order['id'], order_by_product))
    return orders_by_userid_total_price


users_stuff = get_users_stuff('admin')
if users_stuff:
    for item in users_stuff:
        print(item)
else:
    print(0)

print(len(connection.queries), 'db connections')
# В принципе в выводе по названию ключей уже все видно и понятно, можно конечно вывод оформить лучше
