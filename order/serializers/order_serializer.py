from rest_framework import serializers

from order.models import Order
from product.models import Product 
from product.serializers.product_serializer import ProductSerializer

class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(required=True, many=True)
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        total = sum([product.price for product in instance.products.all()])
        return total
    
    class Meta:
        model = Order
        fields = ['products', 'total']