from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListAPI.as_view()),                       # GET /api/v1/products/
    path('<int:pk>/', views.ProductDetailAPI.as_view()),            # GET /api/v1/products/1/
    path('<int:pk>/subscribe/', views.ProductSubscribeAPI.as_view()),  # POST /api/v1/products/1/subscribe/
    path('save-deposit-products/', views.save_deposit_products),
    path('deposit-products/', views.deposit_products),
    path('deposit-product-options/<str:fin_prdt_cd>/', views.deposit_product_options),
    path('deposit-products/top-rate/', views.top_rate),
    path('saving-products/', views.saving_products),                  # GET /api/v1/saving-products/
    
]
