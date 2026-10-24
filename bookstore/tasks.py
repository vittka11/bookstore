from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.utils import timezone

from celery import shared_task

from orders.models import Order


@shared_task
def send_order_email(email, order_id):
    """Send an order confirmation email asynchronously."""
    send_mail(
        subject=f"Order #{order_id}",
        message=f"Your order #{order_id} has been created successfully.",
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )


@shared_task
def generate_daily_report():
    """Generate a simple daily orders report."""
    today = timezone.now().date()

    orders = Order.objects.filter(created__date=today)

    report = {
        "date": str(today),
        "orders_count": orders.count(),
        "paid_orders": orders.filter(paid=True).count(),
    }

    return report


@shared_task
def cleanup_expired_sessions():
    """Delete expired Django sessions."""
    Session.objects.filter(expire_date__lt=timezone.now()).delete()
