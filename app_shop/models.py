
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save


class Product(models.Model):
    """
    model product
    """
    name = models.CharField('Product:', max_length=140)
    price = models.DecimalField('Price', default=0, decimal_places=2,
                                max_digits=11)  # не знаю больше 2 вроде не требуется
    additional_product_group = models.ManyToManyField('QuantityProduct', blank=True)

    class META:
        verbose_name = 'Product'
        verbose_name_plural = 'Product'

    def __str__(self):
        return f'{self.name} - {self.price}'


class QuantityProduct(models.Model):
    """
    model for add extra product in Product model
    """
    additional_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Quantity:', default=1, blank=False, null=False)
    additional_price = models.DecimalField('Additional price', default=0, decimal_places=2, max_digits=11)

    class META:
        verbose_name = 'QuantityProduct'
        verbose_name_plural = 'QuantityProduct'

    def __str__(self):
        return f'{self.additional_product.name} - {self.quantity}'

    def save(self, *args, **kwargs):
        self.additional_price = self.additional_product.price * self.quantity
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, related_name="product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('quantity', default=1)
    price = models.DecimalField('Price', default=0, decimal_places=2, max_digits=11)

    class META:
        verbose_name = 'OrderItem'
        verbose_name_plural = 'OrderItem'

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        super().save(*args, **kwargs)


class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ManyToManyField(OrderItem)

    class META:
        verbose_name = 'Orders'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return self.buyer.username


# signals


def product_quantity_change(sender, instance, *args, **kwargs) -> None:
    current_price = sender.objects.get(pk=instance.pk).additional_product.price * sender.objects.get(
        pk=instance.pk).quantity
    prod = Product.objects.filter(additional_product_group=instance.pk).first()
    if prod:
        prod.price -= current_price
        prod.save()


def additional_product_quantity_setup(sender, instance, *args, **kwargs) -> None:
    prod = Product.objects.filter(additional_product_group=instance.pk).first()
    if prod:
        prod.price += instance.additional_price
        prod.save()


def product_price_change(sender, instance, *args, **kwargs) -> None:
    previous_price = sender.objects.get(pk=instance.pk).price
    to_change_products = QuantityProduct.objects.filter(additional_product=sender.objects.get(pk=instance.pk))
    to_save_products = []
    for item in to_change_products:
        prod = Product.objects.filter(additional_product_group=item.pk).first()
        if prod:
            if instance.price != previous_price:
                prod.price -= previous_price * item.quantity
                prod.price += instance.price * item.quantity
                to_save_products.append(prod)
    sender.objects.bulk_update(to_save_products, fields=['price'])


pre_save.connect(product_quantity_change, sender=QuantityProduct)
pre_save.connect(additional_product_quantity_setup, sender=QuantityProduct)
pre_save.connect(product_price_change, sender=Product)
