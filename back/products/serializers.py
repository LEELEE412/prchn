# products/serializers.py
from rest_framework import serializers
from .models import Product, DepositProducts, DepositOptions

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
          'id','product_id','name','bank_name',
          'intr_rate','supr_rate','save_trm',
          'dcls_month','dcls_strt_day','dcls_end_day',
          'fin_co_no','join_deny','join_way',
          'spcl_cnd','etc_note',
        ]
class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ('product',)  

class DepositProductsSerializer(serializers.ModelSerializer):
    options = DepositOptionsSerializer(many=True, read_only=True)
    class Meta:
        model = DepositProducts
        fields = '__all__'


