from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from catalog.views import (
    HomeView,
    ContactsView,
    ProductDetailView,
    AddProductView,
)

urlpatterns = [
    # 🏠 Главная страница со списком товаров (ListView)
    path("", HomeView.as_view(), name="home"),
    # 📞 Страница "Контакты" с формой обратной связи (TemplateView)
    path("contacts/", ContactsView.as_view(), name="contacts"),
    # 📦 Страница отдельного товара (DetailView)
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    # ➕ Добавление нового товара (CreateView)
    path("add-product/", AddProductView.as_view(), name="add_product"),
]

# 🖼 Подключение статических путей для отображения загруженных изображений при DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# FBV routing version
# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path("", views.home_view, name="home"),
#     path("contacts/", views.contacts_view, name="contacts"),
#     path("product/<int:pk>/", views.product_detail_view, name="product_detail"),
#     path("add-product/", views.add_product_view, name="add_product"),
# ]
