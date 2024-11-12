from django import forms
from .models import Offer, OfferProduct, Product

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['customer', 'description', 'delivery', 'remarks']

class OfferProductForm(forms.ModelForm):
    class Meta:
        model = OfferProduct
        fields = ['product', 'quantity']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity']