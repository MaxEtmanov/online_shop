from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('category/<int:category_id>/', views.product_list, name='by_category'), 
]