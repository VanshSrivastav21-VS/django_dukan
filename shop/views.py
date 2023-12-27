from django.shortcuts import render
from .models import Product, Brand, Category, ProductImage, ProductReview
from .filters import ProductFilter
from django.contrib import messages

def all_products(request):
    f = ProductFilter(request.GET, queryset=Product.objects.all())
    return render(request,'shop/products.html',{
        'filter': f,
        'brands': Brand.objects.filter(favorite=True),
        'categories': Category.objects.all()
    })

def brand_products(request, brand):
    brandObj = Brand.objects.get(slug=brand)
    products=Product.objects.filter(brand=brandObj)
    return render(request,'shop/brand_products.html',{
        'brand': brandObj,
        'products': products,
        'brands': Brand.objects.all(),
        'categories': Category.objects.all()
    })

def category_products(request, category):
    catObj = Category.objects.get(slug=category)
    products=Product.objects.filter(category=catObj)
    return render(request,'shop/category_products.html',{
        'category': catObj,
        'products':products, 
        'brands': Brand.objects.all(),
        'categories': Category.objects.all()
    })

def search_products(request):
    q = request.GET.get('q')
    if q is None:
        messages.error(request, 'Please entre something to search!')
    products_list_1 = Product.objects.filter(name__icontains=q)
    products_list_2 = Product.objects.filter(brand__name__icontains=q)
    products_list_3 = Product.objects.filter(category__name__icontains=q)
    return render(request,'shop/search.html',{
        'products': products_list_1.union(products_list_2, products_list_3),
        'brands': Brand.objects.filter(name__icontains=q),
        'categories': Category.objects.filter(name__icontains=q),
        'q': q,
        'total_items': products_list_1.count() + products_list_2.count() + products_list_3.count()
    })

def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    sim_cat_prod = Product.objects.filter(category=product.category).exclude(slug=slug).order_by('?')[:2]

    reviews = ProductReview.objects.filter(product=product)
    images = ProductImage.objects.filter(product=product)

    return render(request,'shop/product_detail.html',{
        'product': product,
        'images': images,
        'reviews': reviews,
        'sim_cat_prod': sim_cat_prod,
    })
