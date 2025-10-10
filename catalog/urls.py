from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("contacts/", views.contacts_view, name="contacts"),
    path("product/<int:pk>/", views.product_detail_view, name="product_detail"),
    path("add-product/", views.add_product_view, name="add_product"),
]
