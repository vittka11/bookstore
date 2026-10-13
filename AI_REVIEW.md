# AI Code Review

This document describes the AI-assisted code review performed for the Bookstore project.

Three complex views from `orders/views.py` were selected for review:

1. `order_create`
2. `create_checkout_session`
3. `payment_success`

The code was reviewed with ChatGPT. The recommendations were checked before being applied, and the project tests were run after the changes.

---

## 1. order_create

### Original code

```python
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
                order_id=order.id
            )
    else:
        form = OrderCreateForm()

    return render(
        request,
        'orders/order_create.html',
        {'cart': cart, 'form': form}
    )
```

### AI recommendations

- Prevent creation of an order when the shopping cart is empty.
- Use `bulk_create()` instead of executing a separate INSERT query for every order item.
- Send the confirmation email with `transaction.on_commit()` so the email is sent only after the database transaction succeeds.
- Add a docstring describing the purpose of the view.
- Keep the order creation inside `transaction.atomic()`.

### Final code

```python
def order_create(request):
    """Create an order from the current shopping cart."""
    cart = Cart(request)

    if not len(cart):
        return redirect("orders:cart_detail")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)

        if form.is_valid():
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
```

---

## 2. create_checkout_session

### Original code

```python
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
```

### AI recommendations

- Do not create another Stripe Checkout session for an order that is already paid.
- Use `select_related("book")` when loading order items to avoid additional database queries for each book.
- Add a descriptive docstring.
- Keep Stripe configuration in Django settings/environment variables.

### Final code

```python
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
        success_url=request.build_absolute_uri(
            "/orders/payment/success/"
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(
            "/orders/payment/cancel/"
        ),
        metadata={
            "order_id": str(order.id)
        },
    )

    return redirect(session.url, code=303)
```

---

## 3. payment_success

### Original code

```python
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
```

### AI recommendations

- Check that `session_id` exists before requesting data from Stripe.
- Use `.get()` for Stripe metadata instead of direct dictionary access.
- Avoid an unnecessary database UPDATE if the order is already marked as paid.
- Add a docstring describing the payment verification process.

### Final code

```python
def payment_success(request):
    """Verify a Stripe payment and mark the related order as paid."""
    stripe.api_key = settings.STRIPE_SECRET_KEY

    session_id = request.GET.get("session_id")

    if not session_id:
        return redirect("catalog:book_list")

    session = stripe.checkout.Session.retrieve(session_id)

    order_id = session.metadata.get("order_id")
    order = get_object_or_404(Order, id=order_id)

    if session.payment_status == "paid" and not order.paid:
        order.paid = True
        order.save(update_fields=["paid"])

    return render(
        request,
        "orders/payment_success.html",
        {"order": order},
    )
```

---

## Verification

After applying the reviewed changes, the Django system check and automated test suite were executed.

Result:

```text
System check identified no issues (0 silenced).
39 passed
```

One existing email integration test was updated to execute Django `on_commit` callbacks because the reviewed implementation now sends confirmation emails only after a successful transaction.

All AI recommendations were reviewed before being applied to the project.