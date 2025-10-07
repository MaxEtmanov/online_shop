from django.db.models import Sum
from .models import CartItem
from orders.models import Order  # при желании считаем и заказы

def cart_and_order_counts(request):
    """
    Возвращает:
      - cart_count: суммарное количество штук в корзине для текущего пользователя (int)
      - orders_count: количество оформленных заказов пользователя (int)
    Доступно во всех шаблонах после включения процессора в settings.TEMPLATES.
    """
    cart_count = 0
    orders_count = 0

    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        agg = CartItem.objects.filter(user=user).aggregate(total=Sum('quantity'))
        cart_count = agg['total'] or 0
        orders_count = Order.objects.filter(user=user).count()

    return {
        'cart_count': cart_count,
        'orders_count': orders_count,
    }