# back/chat/views.py

import json
import re
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from openai import OpenAI
from products.models import SavingProducts, SavingOptions, DepositOptions, DepositProducts  # 여러분의 앱 경로에 맞춰 수정하세요
from products.serializers import SavingProductsSerializer, SavingOptionsSerializer, DepositProductsSerializer, DepositOptionsSerializer

logger = logging.getLogger(__name__)
client = OpenAI()  # settings.py에 API 키 설정 필요

class RecommendChatView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_msg = (request.data.get("message") or "").strip()
        if not user_msg:
            return Response({"detail": "메시지를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 1) DB에서 예·적금 옵션 샘플 가져와 prompt 에 포함
        qs = DepositOptions.objects.select_related("product").all()[:30]
        options = []
        for o in qs:
            options.append({
                "code":       o.fin_prdt_cd,
                "company":    o.product.kor_co_nm,
                "name":       o.product.fin_prdt_nm,
                "rate":       o.intr_rate,
                "max_rate":   o.intr_rate2,
                "term":       o.save_trm,
            })

        system_prompt = "당신은 금융상품 추천 전문가입니다."
        user_prompt = (
            f"사용자 요청: {user_msg}\n"
            "아래 옵션 중에서 사용자에게 가장 적합한 단 한 개의 예·적금 상품을 "
            "JSON 객체 형식으로, 필드(code, company, name, rate, max_rate, term)만 포함해서 추천해주세요.\n"
            + json.dumps(options, ensure_ascii=False)
        )

        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=300,
            )
            raw = resp.choices[0].message.content

            # 2) GPT 응답에서 ```json ... ``` 블록 파싱
            m = re.search(r"```(?:json)?\s*([\s\S]+?)```", raw, re.IGNORECASE)
            json_str = m.group(1) if m else raw

            try:
                rec = json.loads(json_str)
            except json.JSONDecodeError:
                # 파싱 실패 시 원본 raw 텍스트만 돌려줌
                return Response(
                    {"detail": "추천 결과 파싱 실패", "raw": raw},
                    status=status.HTTP_200_OK
                )

            code = rec.get("code")
            if not code:
                return Response(
                    {"detail": "추천된 상품 코드가 없습니다.", "raw": raw},
                    status=status.HTTP_200_OK
                )

            # 3) DB에서 실제 상품 및 옵션 불러오기
            product = DepositProducts.objects.get(fin_prdt_cd=code)
            prod_ser = DepositProductsSerializer(product)
            opts = DepositOptions.objects.filter(product=product).order_by("save_trm")
            opt_ser = DepositOptionsSerializer(opts, many=True)

            full_product = prod_ser.data
            full_product["options"] = opt_ser.data

            # 4) 클라이언트에 설명(raw) + full_product 전송
            return Response({
                "explanation": raw,
                "product": full_product
            })

        except Exception as e:
            logger.exception("추천 생성 중 오류")
            return Response(
                {"detail": "서버 오류가 발생했습니다.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
