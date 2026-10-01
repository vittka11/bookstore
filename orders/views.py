from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db import transaction

from catalog.models import Book
from .cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem

import stripe

from django.conf import settings

from django.core.mail import send_mail

@require_POST
def cart_add(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)

    cart.add(book=book, quantity=1)

    return redirect('orders:cart_detail')


@require_POST
def cart_remove(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)

    cart.remove(book)

    return redirect('orders:cart_detail')


@require_POST
def cart_clear(request):
    cart = Cart(request)
    cart.clear()

    return redirect('orders:cart_detail')


def cart_detail(request):
    cart = Cart(request)

    return render(
        request,
        'orders/cart_detail.html',
        {'cart': cart}
    )
def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                order = form.save()

                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        book=item['book'],
                        price=item['price'],
                        quantity=item['quantity']
                    )
            send_mail(
                subject=f'Order #{order.id} created',
                message=f'Thank you for your order! Your order number is {order.id}.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.email],
                fail_silently=False,
            )

            cart.clear()
            return redirect(
                'orders:create_checkout_session',
                order_id=order.id,
            )
    else:
        form = OrderCreateForm()

    return render(
        request,
        'orders/order_create.html',
        {
            'cart': cart,
            'form': form
        }
    )

def create_checkout_session(request, order_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    order = get_object_or_404(Order, id=order_id)

    session = stripe.checkout.Session.create(
        mode='payment',
        customer_email=order.email,
        line_items=[
            {
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': item.book.title,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': item.quantity,
            }
            for item in order.items.all()
        ],
        success_url=request.build_absolute_uri(
            '/orders/payment/success/'
        ) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(
            '/orders/payment/cancel/'
        ),
        metadata={
            'order_id': str(order.id)
        }
    )

    return redirect(session.url, code=303)

def payment_success(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    session_id = request.GET.get('session_id')

    session = stripe.checkout.Session.retrieve(session_id)

    order_id = session.metadata['order_id']
    order = get_object_or_404(Order, id=order_id)

    if session.payment_status == 'paid':
        order.paid = True
        order.save(update_fields=['paid'])

    return render(
        request,
        'orders/payment_success.html',
        {'order': order}
    )

def payment_cancel(request):
    return render(request, 'orders/payment_cancel.html')