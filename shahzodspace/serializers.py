from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'user', 'photo', 'item_number', 'name', 'model', 'quantity', 'purchase_price', 'selling_price']

        
