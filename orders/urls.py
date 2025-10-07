from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_view, name='cart_view'),                       # /orders/cart/
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # POST
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),  # POST
    path('checkout/', views.checkout, name='checkout'),                    # GET/POST
    path('my/', views.order_list, name='order_list'),                      # /orders/my/ — список пользователя
    path('<int:order_id>/', views.order_detail, name='order_detail'),      # /orders/123/ — детали заказа
]