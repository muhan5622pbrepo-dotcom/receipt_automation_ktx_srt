async def _extract_filename_from_popup(self, popup_tab):
        """팝업창에서 금액과 날짜 추출 - JavaScript 사용"""
        try:
            # 금액 추출 - JavaScript
            amount_js = f"""
            (function() {{
                var elem = document.querySelector('{CSS.POPUP_AMOUNT}');
                return elem ? elem.textContent : null;
            }})()
            """
            amount_raw = await popup_tab.evaluate(amount_js)
            
            # 날짜 추출 - JavaScript  
            date_js = f"""
            (function() {{
                var elem = document.querySelector('{CSS.POPUP_DATE}');
                return elem ? elem.textContent : null;
            }})()
            """
            date_raw = await popup_tab.evaluate(date_js)
            
            if amount_raw and date_raw:
                # 금액 정리
                amount = re.sub(r'[\n\r\t]+', ' ', amount_raw)
                amount = re.sub(r'\s+', ' ', amount).strip()
                amount_cleaned = re.sub(r'[^0-9]', '', amount)
                
                # 여정 정보 정리
                journey_info = re.sub(r'[\n\r\t]+', ' ', date_raw)
                journey_info = re.sub(r'\s+', ' ', journey_info).strip()
                
                # → 를 " - "로 변경
                journey_cleaned = journey_info.replace("→", " - ")
                
                # 콜론 제거 (시간의 :)
                journey_cleaned = journey_cleaned.replace(":", "")
                
                # 파일명 생성: SRT_여정정보_금액
                # 예: SRT_2026-02-12 SRT 661 일반실 수서(1611) - 나주(1806)_41600
                filename = f"SRT_{journey_cleaned}_{amount_cleaned}"
                
                # Windows 금지 문자만 제거 (하이픈, 공백, 괄호는 유지)
                filename = re.sub(r'[<>"/\\|?*\x00-\x1f]', '', filename)
                
                log(f"생성된 파일명: {filename}")
                return filename
            else:
                log(f"데이터 추출 실패 - amount: {amount_raw}, date: {date_raw}")
            
        except Exception as e:
            log(f"파일명 추출 중 오류: {e}")
        
        return None
