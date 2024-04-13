from django.urls import path
from . import views
from .views import (
    register,
    product_list,
    ProductCreate,
    ProductUpdate,
    ProductList,
    ProductDetail,
    profile,
    add_category,
    category_list,
    product_edit,
    change_password,
    return_product,
    export_sales_report,
    subscription_required_view,
)

from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='shahzodspace/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('products/', product_list, name='product_list'),
    path('products/add/', ProductCreate.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', ProductUpdate.as_view(), name='product_edit'),
    path('add_category/', add_category, name='add_category'),  # Исправлено
    path('categories/', category_list, name='category_list'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('export_products/', views.export_products_to_excel, name='export_products'),
    path('products/<int:pk>/sell/', views.sell_product, name='sell_product'),
    path('password_change/', change_password, name='change_password'),
    path('sales/history/', views.history_of_sales, name='history_of_sales'),
    path('products/return/<int:sale_id>/', return_product, name='return_product'),
    path('subscription_required/', views.subscription_required_view, name='subscription_required'),
    path('export-sales-report/', export_sales_report, name='export_sales_report'),
    path('api/products/', ProductList.as_view(), name='product-list'),
    path('api/products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
]
