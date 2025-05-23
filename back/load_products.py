# load_products.py
import os
import django
import requests
import warnings

# SSL 인증 경고 무시
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Django 설정 로드
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.conf import settings
from products.models import Product


def fetch_all_products(group_no: str, endpoint: str) -> list:
    """
    주어진 금융상품 그룹번호(topFinGrpNo)와 엔드포인트 파일명으로
    전체 페이지를 순회하며 baseList를 모두 수집합니다.
    """
    items = []
    page = 1
    while True:
        res = requests.get(
            f"https://finlife.fss.or.kr/finlifeapi/{endpoint}",
            params={
                'auth': settings.FINLIFE_API_KEY,
                'topFinGrpNo': group_no,
                'pageNo': page,
                'pageNoCnt': 1000,
            },
            verify=False
        )
        res.raise_for_status()
        data = res.json().get('result', {})
        batch = data.get('baseList', [])
        if not batch:
            break

        items.extend(batch)
        max_page = int(data.get('max_page_no', 1))
        if page >= max_page:
            break
        page += 1

    return items


def main():
    # API 키 확인
    print("🔑 FINLIFE_API_KEY:", repr(settings.FINLIFE_API_KEY))

    # 예금(020000) + 적금(020001) 전체 데이터 수집
    deposit_items = fetch_all_products('020000', 'depositProductsSearch.json')
    saving_items  = fetch_all_products('020001', 'savingProductsSearch.json')
    all_items = deposit_items + saving_items

    print(f"🔄 총 수집된 상품 건수: {len(all_items)}")
    if all_items:
        print(all_items[0])  # 첫 번째 항목 샘플 출력

    created = 0
    for it in all_items:
        pid = it.get('fin_prdt_cd')
        trm = int(it.get('save_trm') or 0)

        # API에서 넘어온 모든 키·값을 그대로 defaults에 담습니다.
        defaults = { key: it.get(key) for key in it.keys() }

        obj, was_created = Product.objects.update_or_create(
            product_id=pid,
            save_trm=trm,
            defaults=defaults
        )
        if was_created:
            created += 1

    print(f"✅ 새로 생성된 상품 수: {created}")


if __name__ == '__main__':
    main()
