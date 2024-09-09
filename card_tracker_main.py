import pandas as pd
from enum import Enum
import os
import webbrowser
import sys

# Enum 클래스 정의
class CardIndex(Enum):
    SHINHAN_CREDIT = 0
    SHINHAN_CHECK = 1
    KB = 2
    WOORI = 3
    HANA = 4
    NH = 5
    SAMSUNG = 6

CARD_NAMES = {
    CardIndex.SHINHAN_CREDIT: "[신한 카드(신용)]",
    CardIndex.SHINHAN_CHECK: "[신한 카드(체크)]",
    CardIndex.KB: "[국민 카드]",
    CardIndex.WOORI: "[우리 카드]",
    CardIndex.HANA: "[하나 카드]",
    CardIndex.NH: "[농협 카드]",
    CardIndex.SAMSUNG: "[삼성 카드]"
}

CARD_URLS = {
    CardIndex.SHINHAN_CREDIT: "https://www.shinhancard.com/mob/MOBFM043N/MOBFM043R01.shc?vname=MOBFM043R03&nextMonthYn=N",
    CardIndex.SHINHAN_CHECK: "https://www.shinhancard.com/mob/MOBFM043N/MOBFM043R01.shc?vname=MOBFM043R03&nextMonthYn=N",
    CardIndex.KB: "https://www.kbcard.com",
    CardIndex.WOORI: "https://pc.wooricard.com/dcpc/yh1/mcd/mcd02/H1MCD202S00.do",
    CardIndex.HANA: "https://www.hanacard.com",
    CardIndex.NH: "https://www.nhcard.com",
    CardIndex.SAMSUNG: "https://www.samsungcard.com"
}
# 상수 정의
DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
CANCEL_KEYWORDS_1 = '취소'
CANCEL_KEYWORDS_2 = '메가엠지씨커피|카페|ＳＫＴ|더벤티|교통|에스케이텔레콤|우드진|카페무아르'

# 파일 경로 생성 함수
def get_file_path(file_name):
    return os.path.join(DOWNLOADS_DIR, file_name)

# 파일 경로 확인 및 URL 실행 함수
def check_file_and_open_url(file_path, url):
    if not os.path.exists(file_path):
        print(f"파일이 존재하지 않습니다: {file_path}\n")
        print(f"브라우저에서 URL을 실행합니다: {url}\n")
        webbrowser.open(url)  # 브라우저에서 URL 열기
        sys.exit("파일이 없어 프로그램을 종료합니다.\n")  # 프로그램 종료
    else:
        print(f"파일이 존재합니다: {file_path}\n")

# 파일 저장 및 읽기 함수
def save_output_to_file(output_text, file_name="output.txt"):
    with open(file_name, "w", encoding="utf-8") as file:
        file.write("\n".join(output_text))

    with open(file_name, "r", encoding="utf-8") as file:
        print(file.read())

# 금액 처리 함수
def process_transactions(df, amount_col, status_col, cancel_keywords, transaction_type):
    df[amount_col] = df[amount_col].replace(',', '', regex=True).astype(float)

    cancelled_transactions = df[df[status_col].str.contains(cancel_keywords, case=False, na=False)]
    total_cancelled_amount = cancelled_transactions[amount_col].sum()
    output_text.append(f"{transaction_type} 취소 금액: {total_cancelled_amount}")

    valid_transactions = df[~df[status_col].str.contains(cancel_keywords, case=False, na=False)]
    total_amount = valid_transactions[amount_col].sum()
    output_text.append(f"{transaction_type} 이용 금액: {total_amount}")

    return total_amount

# 카드 인덱스 확인 함수
def check_card_index(card_index):
    return CARD_NAMES.get(card_index, "[알 수 없는 카드]")

# 실행 코드
card_index = CardIndex.SHINHAN_CREDIT
output_text = []
total_amount_sum = 0

output_text.append("======================================================")
output_text.append(check_card_index(card_index))

# 첫 번째 파일 처리
card_url = CARD_URLS.get(card_index, "https://www.naver.com")
check_file_and_open_url(get_file_path("신용카드이용내역_승인_국내통합.xls"), card_url)

df = pd.read_excel(get_file_path("신용카드이용내역_승인_국내통합.xls"), engine='xlrd')
df.columns = df.columns.str.strip()

if '이용금액' in df.columns:
    if card_index == CardIndex.SHINHAN_CREDIT:  # 더모아 카드를 사용하는 경우 5000원 이상일 때 백원단위는 캐시백이 된다.
        df['이용금액'] = df['이용금액'].apply(lambda x: (x // 1000) * 1000 if x > 5000 else x)

    total_amount_sum = process_transactions(df, '이용금액', '매입상태', CANCEL_KEYWORDS_1, "결제")
else:
    output_text.append("이용금액 열을 찾을 수 없습니다.")

# 두 번째 파일 처리
card_index = CardIndex.WOORI
card_url = CARD_URLS.get(card_index, "https://www.naver.com")
check_file_and_open_url(get_file_path("report.xls"), card_url)

df_2 = pd.read_excel(get_file_path("report.xls"), header=1, engine='xlrd')
df_2.columns = df_2.columns.str.strip()

if '이용금액(원)' in df_2.columns:
    output_text.append("\n" + check_card_index(card_index))
    total_amount_sum += process_transactions(df_2, '이용금액(원)', '이용가맹점(은행)명', CANCEL_KEYWORDS_2, "개인(공과금)")
else:
    output_text.append("이용금액(원) 열을 찾을 수 없습니다.")

while True:
    subtract_amount_input = input("추가로 뺄 금액이 있습니까? (금액을 입력하거나, 없으면 '0'을 입력하세요): ")
    try:
        subtract_amount = int(subtract_amount_input)
        if subtract_amount == 0:
            break
        total_amount_sum -= subtract_amount
        output_text.append(f"추가로 뺀 금액: {subtract_amount}")
        if subtract_amount > 0:
            break;
    except ValueError:
        print("유효한 금액을 입력해주세요.")

output_text.append(f"\n총 청구 금액: {total_amount_sum}")
output_text.append("======================================================")

# 결과 파일로 저장 및 출력
save_output_to_file(output_text)