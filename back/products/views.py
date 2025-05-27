from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import DepositProducts, SavingProducts
from .serializers import DepositProductsSerializer, SavingProductsSerializer, DepositOptionsSerializer, SavingOptionsSerializer
import requests
from django.conf import settings

# ── 1) 예금 상품 목록
class DepositProductsListAPI(generics.ListAPIView):
    queryset = DepositProducts.objects.prefetch_related('options').all()
    serializer_class = DepositProductsSerializer

class DepositProductsFetchAPI(generics.GenericAPIView):
    """
    외부 API에서 예금 상품(baseList)과 옵션(optionList)을 
    받아와서 DB에 저장/업데이트하는 엔드포인트입니다.
    """
    # queryset 이나 serializer_class 를 설정하면, 
    # GenericAPIView 가 내부적으로 get_object/get_serializer 를 지원합니다.
    permission_classes = [AllowAny]
    queryset = DepositProducts.objects.all()
    serializer_class = DepositProductsSerializer

    def post(self, request, *args, **kwargs):
        # 1) 외부 API 호출
        url = (
            f"https://finlife.fss.or.kr/finlifeapi/"
            f"depositProductsSearch.json?auth={settings.FINLIFE_API_KEY}"
            f"&topFinGrpNo=020000&pageNo=1"
        )
        result = requests.get(url).json().get('result', {})
        base_list   = result.get('baseList', [])
        option_list = result.get('optionList', [])

        # 2) baseList 처리: DepositProducts 저장
        for item in base_list:
            serializer = DepositProductsSerializer(data={
                'fin_prdt_cd': item.get('fin_prdt_cd'),
                'kor_co_nm':   item.get('kor_co_nm', ''),
                'fin_prdt_nm': item.get('fin_prdt_nm', ''),
                'etc_note':    item.get('etc_note', ''),
                'join_deny':   int(item.get('join_deny') or 1),
                'join_member': item.get('join_member', ''),
                'join_way':    item.get('join_way', ''),
                'spcl_cnd':    item.get('spcl_cnd', ''),
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()

        # 3) optionList 처리: DepositOptions 저장 (FK 연결)
        for opt in option_list:
            parent = DepositProducts.objects.get(fin_prdt_cd=opt.get('fin_prdt_cd'))
            opt_serializer = DepositOptionsSerializer(data={
                'intr_rate_type_nm': opt.get('intr_rate_type_nm', ''),
                'intr_rate':         float(opt.get('intr_rate')  or -1),
                'intr_rate2':        float(opt.get('intr_rate2') or -1),
                'save_trm':          int(opt.get('save_trm') or 0),
            })
            opt_serializer.is_valid(raise_exception=True)
            opt_serializer.save(product=parent)

        return Response(
            {'message': 'Deposit data synced.'},
            status=status.HTTP_201_CREATED
        )

# ── 3) 적금 상품 목록
class SavingProductsListAPI(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset           = SavingProducts.objects.prefetch_related('options').all()
    serializer_class   = SavingProductsSerializer

class SavingProductsFetchAPI(generics.GenericAPIView):
    """
    외부 API에서 적금 상품(baseList)과 옵션(optionList)을
    받아와서 DB에 저장/업데이트하는 엔드포인트입니다.
    """
    # ◀— 여기는 무조건 클래스 레벨!
    permission_classes = [AllowAny]
    queryset           = SavingProducts.objects.all()
    serializer_class   = SavingProductsSerializer

    def post(self, request, *args, **kwargs):
        # 1) 외부 API 호출
        url = (
            f"https://finlife.fss.or.kr/finlifeapi/"
            f"savingProductsSearch.json?auth={settings.FINLIFE_API_KEY}"
            f"&topFinGrpNo=020000&pageNo=1"
        )
        result      = requests.get(url).json().get('result', {})
        base_list   = result.get("baseList", [])
        option_list = result.get("optionList", [])

        # 2) baseList 처리: SavingProducts 저장/업데이트
        for item in base_list:
            serializer = SavingProductsSerializer(data={
                "fin_prdt_cd": item.get("fin_prdt_cd"),
                "kor_co_nm":   item.get("kor_co_nm", ""),
                "fin_prdt_nm": item.get("fin_prdt_nm", ""),
                "etc_note":    item.get("etc_note", ""),
                "join_deny":   int(item.get("join_deny") or 1),
                "join_member": item.get("join_member", ""),
                "join_way":    item.get("join_way", ""),
                "spcl_cnd":    item.get("spcl_cnd", ""),
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()

        # 3) optionList 처리: SavingOptions 저장 (FK 연결)
        for opt in option_list:
            parent = SavingProducts.objects.get(fin_prdt_cd=opt.get("fin_prdt_cd"))
            opt_serializer = SavingOptionsSerializer(data={
                "intr_rate_type_nm": opt.get("intr_rate_type_nm", ""),
                "intr_rate":         float(opt.get("intr_rate")  or -1),
                "intr_rate2":        float(opt.get("intr_rate2") or -1),
                "save_trm":          int(opt.get("save_trm") or 0),
            })
            opt_serializer.is_valid(raise_exception=True)
            opt_serializer.save(product=parent)

        return Response(
            {"message": "Saving data synced."},
            status=status.HTTP_201_CREATED
        )