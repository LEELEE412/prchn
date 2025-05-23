import requests
import os
from dotenv import load_dotenv
from pprint import pprint

import environ

# .env에서 API_KEY 불러오기
load_dotenv()
API_KEY = os.getenv("FINLIFE_API_KEY ")

# 금융감독원 정기예금 API 호출
url = f"https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1"

response = requests.get(url)
data = response.json()

# 전체 응답 pprint로 출력
print("===== 전체 응답 =====")
pprint(data)

# # baseList 따로 출력
# print("\n===== 상품 목록 (baseList) =====")
# pprint(data.get('result', {}).get('baseList', []))

# # optionList 따로 출력
# print("\n===== 옵션 목록 (optionList) =====")
# pprint(data.get('result', {}).get('optionList', []))
