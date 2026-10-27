from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db import transaction

from catalog.models import Book
from .cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem
from .warehouse_service import WarehouseServiceError, reserve_stock

import stripe

from django.conf import settings

from django.core.mail import send_mail
import logging
logger = logging.getLogger(__name__)


@require_POST
def cart_add(request, book_id):
    """Add a book to the shopping cart."""
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)

    cart.add(book=book, quantity=1)

    return redirect("orders:cart_detail")


@require_POST
def cart_remove(request, book_id):
    """Remove a book from the shopping cart."""
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)

    cart.remove(book)

    return redirect("orders:cart_detail")


@require_POST
def cart_clear(request):
    """Remove all books from the shopping cart."""
    cart = Cart(request)
    cart.clear()

    return redirect("orders:cart_detail")


def cart_detail(request):
    """Display the current shopping cart."""
    cart = Cart(request)

    return render(request, "orders/cart_detail.html", {"cart": cart})


def order_create(request):
    """Create an order from the current shopping cart."""
    cart = Cart(request)

    if not len(cart):
        return redirect("orders:cart_detail")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            try:
                for item in cart:
                    reserve_stock(
                        book_id=item["book"].id,
                        quantity=item["quantity"],
                    )
            except WarehouseServiceError:
                form.add_error(
                    None,
                    "Could not reserve books in warehouse. Please try again.",
                )
                return render(
                    request,
                    "orders/order_create.html",
                    {
                        "cart": cart,
                        "form": form,
                    },
                )

            with transaction.atomic():
                order = form.save()

                order_items = [
                    OrderItem(
                        order=order,
                        book=item["book"],
                        price=item["price"],
                        quantity=item["quantity"],
                    )
                    for item in cart
                ]

                OrderItem.objects.bulk_create(order_items)

                transaction.on_commit(
                    lambda: send_mail(
                        subject=f"Order #{order.id} created",
                        message=(
                            f"Thank you for your order! "
                            f"Your order number is {order.id}."
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[order.email],
                        fail_silently=False,
                    )
                )

            cart.clear()

            return redirect(
                "orders:create_checkout_session",
                order_id=order.id,
            )

    else:
        form = OrderCreateForm()

    return render(
        request,
        "orders/order_create.html",
        {
            "cart": cart,
            "form": form,
        },
    )


def create_checkout_session(request, order_id):
    """Create a Stripe Checkout session for an unpaid order."""
    stripe.api_key = settings.STRIPE_SECRET_KEY

    order = get_object_or_404(Order, id=order_id)

    if order.paid:
        return redirect("catalog:book_list")

    session = stripe.checkout.Session.create(
        mode="payment",
        customer_email=order.email,
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": item.book.title,
                    },
                    "unit_amount": int(item.price * 100),
                },
                "quantity": item.quantity,
            }
            for item in order.items.select_related("book").all()
        ],
        success_url=request.build_absolute_uri("/orders/payment/success/")
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri("/orders/payment/cancel/"),
        metadata={"order_id": str(order.id)},
    )

    return redirect(session.url, code=303)


def payment_success(request):
    """Verify a Stripe payment and mark the related order as paid."""
    stripe.api_key = settings.STRIPE_SECRET_KEY

    session_id = request.GET.get("session_id")

    if not session_id:
        return redirect("catalog:book_list")

    try:
        session = stripe.checkout.Session.retrieve(session_id)

        order_id = session.metadata["order_id"]
        order = get_object_or_404(Order, id=order_id)

        if session.payment_status == "paid" and not order.paid:
            order.paid = True
            order.save(update_fields=["paid"])

        return render(
            request,
            "orders/payment_success.html",
            {"order": order},
        )

    except Exception as exc:
        logger.exception("Stripe payment success error: %s", exc)
        return redirect("catalog:book_list")


def payment_cancel(request):
    """Display the payment cancellation page."""
    return render(request, "orders/payment_cancel.html")
