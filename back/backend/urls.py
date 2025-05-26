# backend/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/products/', include('products.urls')),


    # DRF 기본 토큰 발급 (no CSRF)
    path("api/v1/api-token-auth/", obtain_auth_token, name="api-token-auth"),

    # dj-rest-auth 로그인/로그아웃/유저조회
    path("api/v1/accounts/", include("dj_rest_auth.urls")),
    path("api/v1/accounts/registration/", include("dj_rest_auth.registration.urls")),

    # 커뮤니티 API
    path("api/v1/community/", include(("community.urls", "community"), namespace="community")),
    path('api/v1/accounts/', include('accounts.urls')),  # 프로필 엔드포인트 추가
    path('api/v1/accounts/', include('dj_rest_auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
