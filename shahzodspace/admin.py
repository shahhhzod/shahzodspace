from django.contrib import admin
from .models import Product  # Импортируйте другие модели по мере необходимости
from .models import Category
from .models import UserProfile

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(UserProfile)