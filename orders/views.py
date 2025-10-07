from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseNotAllowed
from django.contrib import messages

from products.models import Product
from .models import CartItem, Order, OrderItem

# -------------------------
# Добавление товара в корзину
# -------------------------
@login_required
def add_to_cart(request, product_id):
    """
    Добавить товар в корзину.
    Поведение по завершении: сначала пытаемся перенаправить на request.POST['next'],
    затем на HTTP_REFERER (страница, откуда пришёл запрос), иначе на products:list.
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1
    if quantity < 1:
        quantity = 1

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save(update_fields=['quantity'])

    messages.success(request, f'Товар «{product.name}» добавлен в корзину (кол-во: {quantity}).')

    # куда редиректим: priority = POST 'next' -> HTTP_REFERER -> products:list
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
    if next_url:
        # если next_url — относительный путь вида '/products/...', безопасно редиректить
        return redirect(next_url)
    return redirect('products:list')

# Просмотр корзины
# -------------------------
@login_required
def cart_view(request):
    """
    Показываем все CartItem текущего пользователя.
    Вычисляем общую сумму и передаём в шаблон.
    """
    items = CartItem.objects.filter(user=request.user).select_related('product')
    total = sum([it.get_total_price() for it in items], Decimal('0'))
    return render(request, 'orders/cart.html', {'items': items, 'total': total})


# -------------------------
# Удаление элемента из корзины
# -------------------------
@login_required
@transaction.atomic
def remove_from_cart(request, cart_item_id):
    """Удаление CartItem (POST)."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    ci = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    ci.delete()
    return redirect('orders:cart_view')


# -------------------------
# Оформление заказа (GET — подтверждение, POST — создание заказа)
# -------------------------
@login_required
@transaction.atomic
def checkout(request):
    """
    GET: показываем краткое подтверждение заказа (без картинок).
    POST: создаём Order + OrderItem'ы, уменьшаем stock, очищаем корзину.
    """
    items = CartItem.objects.filter(user=request.user).select_related('product')
    if not items.exists():
        # если корзина пуста — редирект на корзину с сообщением (можно улучшить)
        return redirect('orders:cart_view')

    if request.method == 'GET':
        total = sum([it.get_total_price() for it in items], Decimal('0'))
        return render(request, 'orders/checkout_confirm.html', {'items': items, 'total': total})

    # POST — подтверждение и создание заказа
    order = Order.objects.create(user=request.user, total=Decimal('0'))
    total = Decimal('0')

    for ci in items:
        product = ci.product
        unit_price = product.price or Decimal('0')
        # создаём OrderItem - делаем снэпшот названия и цены
        OrderItem.objects.create(
            order=order,
            product_name=product.name,
            product=product,
            unit_price=unit_price,
            quantity=ci.quantity
        )
        # считаем итог
        total += unit_price * ci.quantity
        # уменьшаем stock, если достаточно; если нет — можно обработать отдельно
        if product.stock >= ci.quantity:
            product.stock -= ci.quantity
            product.save(update_fields=['stock'])
        else:
            # если мало на складе — уменьшаем до нуля (альтернативно: пометить, бросить ошибку и т.д.)
            product.stock = max(0, product.stock - ci.quantity)
            product.save(update_fields=['stock'])

    order.total = total
    order.save(update_fields=['total'])

    # очищаем корзину пользователя
    items.delete()

    # отображаем страницу успеха с информацией о заказе
    return render(request, 'orders/checkout_success.html', {'order': order})


# -------------------------
# Список заказов текущего пользователя
# -------------------------
@login_required
def order_list(request):
    """
    Показываем историю заказов текущего пользователя.
    """
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'orders/order_list.html', {'orders': orders})


# -------------------------
# Детали заказа (только владелец может просматривать)
# -------------------------
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()
    return render(request, 'orders/order_detail.html', {'order': order, 'items': items})