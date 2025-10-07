from django.shortcuts import render, redirect, get_object_or_404

from .models import Product, Category

def product_list(request, category_id=None):
    categories = Category.objects.all()
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=selected_category)
    else:
        selected_category = None
        products = Product.objects.all()
    return render(
        request,
        'products/product_list.html',
        {
            'products': products,
            'categories': categories,
            'selected_category': selected_category,
        }
    )

def home(request):
    # Перенаправляем на список всех продуктов
    return redirect('products:list')