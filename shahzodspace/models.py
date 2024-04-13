from django.db import models
from django.conf import settings
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    trial_start_date = models.DateTimeField(auto_now_add=True)
    subscription_active = models.BooleanField(default=True)  # Предоставление значения по умолчанию

    @property
    def trial_ends(self):
        """Возвращает дату окончания пробного периода."""
        return self.trial_start_date + timedelta(days=7)

    @property
    def days_until_trial_ends(self):
        """Возвращает количество дней до окончания пробного периода."""
        return (self.trial_ends - timezone.now()).days

    def __str__(self):
        return self.user.username + "'s profile"

class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products', null=True)
    photo = models.ImageField(upload_to='products/')
    item_number = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')  # Используйте строковую ссылку, если модель Category определена после модели Product
    name = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class Sale(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='sales')
    quantity = models.PositiveIntegerField(help_text="Количество")
    discount_percentage = models.FloatField(default=0, help_text="Скидка в процентах")
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Цена продажи")
    sale_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.discount_percentage = Decimal(self.discount_percentage) / Decimal('100.00')
        self.sale_price = Decimal(self.quantity) * self.product.selling_price * (Decimal('1.00') - self.discount_percentage)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} шт"