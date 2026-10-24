from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Book


@receiver(post_save, sender=Book)
@receiver(post_delete, sender=Book)
def invalidate_book_cache(sender, instance, **kwargs):
    """Invalidate cached book data when a book changes or is deleted."""
    cache.delete(f"book_detail_{instance.pk}")
    cache.clear()
