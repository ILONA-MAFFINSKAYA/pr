from django.urls import path
from . import views

urlpatterns = [
    path('create_offer/', views.create_offer, name='create_offer'),
    path('offer_detail/<int:offer_id>/', views.offer_detail, name='offer_detail'),
    path('offer_list/', views.offer_list, name='offer_list'),
    path('create_product/', views.create_product, name='create_product'),
    path('product_list/', views.product_list, name='product_list'),
    path('edit_offer/<int:offer_id>/', views.edit_offer, name='edit_offer'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('get-product-details/<int:product_id>/', views.get_product_details, name='get_product_details'),
]