"""
CSS 선택자 설정 파일
SRT 영수증/이용내역 페이지용 CSS 선택자 정의
"""

class CSS:
    # ========================================
    # 영수증/이용내역 페이지
    # URL: https://etk.srail.kr/hpg/hta/03/selectBreakdownList.do?pageId=TK0102030100
    # ========================================
    
    # 승차일자 - 시작일
    DATE_START_YEAR = "#dptDtFromY"      # 시작일 년도 (select 펼침메뉴)
    DATE_START_MONTH = "#dptDtFromM"     # 시작일 월 (select 펼침메뉴)
    DATE_START_DAY = "#dptDtFromD"       # 시작일 일 (select 펼침메뉴)
    
    # 승차일자 - 종료일
    DATE_END_YEAR = "#dptDtToY"          # 종료일 년도 (select 펼침메뉴)
    DATE_END_MONTH = "#dptDtToM"         # 종료일 월 (select 펼침메뉴)
    DATE_END_DAY = "#dptDtToD"           # 종료일 일 (select 펼침메뉴)
    
    # 조회하기 버튼
    SEARCH_BUTTON = "#search-form > fieldset > div.tal_c > button"
    
    # 조회 결과 리스트
    CHECKBOX_TEMPLATE = "#list-form > fieldset > div > table > tbody > tr:nth-child({row}) > td:nth-child(1) > input[type=checkbox]"  # 체크박스
    TICKET_STATUS_TEMPLATE = "#list-form > fieldset > div > table > tbody > tr:nth-child({row}) > td:nth-child(9)"  # 발권상태
    RESULT_ROWS = "#list-form > fieldset > div > table > tbody > tr"  # 전체 결과 행
    
    # 영수증 인쇄 버튼
    PRINT_BUTTON = "#wrap > div.container.container-e > div > div.sub_con_area > div.tal_c > button.btn_large.btn_emerald.fs18.val_m"
    
    # 팝업창 영수증 정보 - 수정된 선택자 (금액과 날짜가 바뀌어 있었음)
    POPUP_AMOUNT = "div.stlm table tbody tr:first-child td"  # 금액 (실제로는 여기가 금액)
    POPUP_DATE = "div.jrny > ul > li"  # 날짜 (여정 정보에서 날짜 추출)
