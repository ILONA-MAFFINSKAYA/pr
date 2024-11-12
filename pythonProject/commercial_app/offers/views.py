from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.dateformat import DateFormat
from .models import Offer, OfferProduct, Product, CustomUser
from .forms import OfferForm, OfferProductForm, ProductForm
from django.http import JsonResponse
import datetime

@login_required
def home_view(request):
    user = request.user
    full_name = user.get_full_name()
    return render(request, 'offers/home.html', {'full_name': full_name})

@login_required
def create_offer(request):
    if request.method == 'POST':
        offer_form = OfferForm(request.POST)
        if offer_form.is_valid():
            offer = offer_form.save(commit=False)
            try:
                offer.executor = request.user.customuser
            except CustomUser.DoesNotExist:
                return render(request, 'offers/create_offer.html', {'error': 'User has no customuser'})

            # Генерируем уникальный номер и текущую дату
            offer.number = f"COM-{Offer.objects.count() + 1}"
            offer.date = datetime.date.today().strftime('%d.%m.%y')
            offer.save()

            # Обработка добавленных продуктов
            for key in request.POST:
                if key.startswith('product-'):
                    product_form = OfferProductForm(request.POST, prefix=key)
                    if product_form.is_valid():
                        offer_product = product_form.save(commit=False)
                        offer_product.offer = offer
                        offer_product.save()

            return redirect('offer_detail', offer_id=offer.id)
    else:
        offer_form = OfferForm()

    offer_products = []
    if request.method == 'POST':
        for key in request.POST:
            if key.startswith('product-'):
                product_form = OfferProductForm(request.POST, prefix=key)
                if product_form.is_valid():
                    offer_product = product_form.save(commit=False)
                    offer_product.offer = offer
                    offer_product.save()
                    offer_products.append(offer_product)
    else:
        for i in range(1):
            offer_products.append(OfferProductForm(prefix=f'product-{i}'))

    products = Product.objects.all()
    context = {
        'offer_form': offer_form,
        'offer_products': offer_products,
        'products': products,
    }
    return render(request, 'offers/create_offer.html', context)

@login_required
def offer_detail(request, offer_id):
    offer = Offer.objects.get(id=offer_id)
    context = {
        'offer': offer,
    }
    return render(request, 'offers/offer_detail.html', context)

@login_required
def offer_list(request):
    offers = Offer.objects.all()
    context = {
        'offers': offers,
    }
    return render(request, 'offers/offer_list.html', context)

@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'offers/create_product.html', {'form': form})

@login_required
def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'offers/product_list.html', context)

@login_required
def edit_offer(request, offer_id):
    offer = Offer.objects.get(id=offer_id)
    if request.method == 'POST':
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('offer_detail', offer_id=offer.id)
    else:
        form = OfferForm(instance=offer)
    return render(request, 'offers/edit_offer.html', {'form': form})

@login_required
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'offers/edit_product.html', {'form': form})

def get_product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    data = {
        'name': product.name,
        'price': product.price
    }
    return JsonResponse(data)