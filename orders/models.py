from django.db import models
from django.utils.translation import gettext_lazy as _
from catalog.models import Book


class Order(models.Model):
    first_name = models.CharField(_("First name"), max_length=100)
    last_name = models.CharField(_("Last name"), max_length=100)
    email = models.EmailField(_("Email"))
    address = models.CharField(_("Address"), max_length=250)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    paid = models.BooleanField(_("Paid"), default=False)

    def __str__(self):
        return f"Order {self.id} - {self.first_name} {self.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name=_("Order")
    )
    book = models.ForeignKey(
        Book,
        related_name='order_items',
        on_delete=models.CASCADE,
        verbose_name=_("Book")
    )
    price = models.DecimalField(
        _("Price"),
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField(
        _("Quantity"),
        default=1
    )

    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.book.title} x {self.quantity}"