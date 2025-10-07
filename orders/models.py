from django.db import models

from django.db import models
from django.conf import settings
from products.models import Product
from decimal import Decimal

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    class Meta:
        unique_together = ('user', 'product')
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'

    def __str__(self):
        return f"{self.user.username}: {self.product.name} x {self.quantity}"

    def get_total_price(self):
        return (self.product.price or Decimal('0')) * self.quantity

class Order(models.Model):
    """
    Оформлённый заказ. total хранится на момент сохранения заказа.
    """
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DONE = 'done'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_NEW, 'Новый'),
        (STATUS_IN_PROGRESS, 'В обработке'),
        (STATUS_DONE, 'Выполнен'),
        (STATUS_CANCELLED, 'Отменён'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} — {self.user.username}"

    def recalc_total(self):
        total = sum([oi.get_total_price() for oi in self.items.all()], Decimal('0'))
        self.total = total
        self.save(update_fields=['total'])

class OrderItem(models.Model):
    """
    Снэпшот строки заказа: копируем имя и цену, чтобы история заказа не зависела от изменения продукта.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Строка заказа'
        verbose_name_plural = 'Строки заказа'

    def __str__(self):
        return f"#{self.order.id} — {self.product_name} x {self.quantity}"

    def get_total_price(self):
        return (self.unit_price or Decimal('0')) * self.quantity