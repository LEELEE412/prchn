# products/serializers.py
from rest_framework import serializers
from .models import Product, DepositProducts, DepositOptions, SavingProducts, SavingOptions

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


class SavingOptionsSerializer(serializers.ModelSerializer):
    # fin_prdt_cd 는 read_only 로 뺐습니다
    fin_prdt_cd = serializers.CharField(source='product.fin_prdt_cd', read_only=True)

    class Meta:
        model  = SavingOptions
        fields = [
            'id',
            'fin_prdt_cd',
            'intr_rate_type_nm',
            'intr_rate',
            'intr_rate2',
            'save_trm',
        ]
        read_only_fields = ['id', 'fin_prdt_cd']

class SavingProductsSerializer(serializers.ModelSerializer):
    # 여기에 옵션을 nested 로 붙여 줍니다
    options = SavingOptionsSerializer(many=True, read_only=True)

    class Meta:
        model  = SavingProducts
        # '__all__' 쓰셔도 되고, 필요한 필드만 나열하셔도 됩니다
        fields = '__all__'