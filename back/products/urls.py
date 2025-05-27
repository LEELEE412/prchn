# products/urls.py
from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    # 1) 예금 상품 목록 조회
    path('deposit-products/', views.DepositProductsListAPI.as_view(), name='deposit-list'),
    # 2) 예금 상품 데이터 외부 API 동기화
    path('deposit-products/fetch/', views.DepositProductsFetchAPI.as_view(), name='deposit-fetch'),

    # 3) 적금 상품 목록 조회
    path('saving-products/', views.SavingProductsListAPI.as_view(), name='saving-list'),
    # 4) 적금 상품 데이터 외부 API 동기화
    path('saving-products/fetch/', views.SavingProductsFetchAPI.as_view(), name='saving-fetch'),
]