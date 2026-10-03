from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"))

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    author = models.CharField(_("Author"), max_length=100)
    price = models.DecimalField(
        _("Price"),
        max_digits=10,
        decimal_places=2
    )
    description = models.TextField(_("Description"))
    stock = models.IntegerField(_("Stock"))
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_("Category")
    )

    def __str__(self):
        return self.title