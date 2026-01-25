from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

from catalog.views import (
    HomeView,
    ContactsView,
    ProductDetailView,
    AddProductView,
    ProductUpdateView,
    ProductDeleteView,
    ProductUnpublishView,
    CategoryProductsView,
)

app_name = "catalog"

# оборачиваем страницу товара в кеш, если включено кеширование
product_detail_view = ProductDetailView.as_view()
if settings.CACHE_ENABLED:
    product_detail_view = cache_page(60 * 15)(product_detail_view)  # 15 минут

urlpatterns = [
    # 🏠 Главная страница со списком товаров (ListView)
    path("", HomeView.as_view(), name="home"),
    # 📞 Страница "Контакты" с формой обратной связи (TemplateView)
    path("contacts/", ContactsView.as_view(), name="contacts"),
    # 📦 Страница отдельного товара (DetailView)
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    # ➕ Добавление нового товара (CreateView)
    # path("products/add/", AddProductView.as_view(), name="product_add"),
    path(
        "add-product/", AddProductView.as_view(), name="add_product"
    ),  # алиас для старого имени!!!
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_edit"),
    path(
        "products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path(
        "<int:pk>/unpublish/", ProductUnpublishView.as_view(), name="product_unpublish"
    ),
    path(
        "category/<int:category_id>/",
        CategoryProductsView.as_view(),
        name="category_products",
    ),
]

# 🖼 Подключение статических путей для отображения загруженных изображений при DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
