"""
JavaScript 코드 모음
SRT 영수증 자동화에 필요한 JavaScript 코드
"""

class JSCode:
    # select 요소 값 설정 및 change 이벤트 발생
    # {selector}: CSS 선택자
    # {value}: 설정할 값
    SELECT_VALUE_AND_TRIGGER_CHANGE = """
    document.querySelector('{selector}').value = '{value}';
    document.querySelector('{selector}').dispatchEvent(new Event('change', {{ bubbles: true }}));
    """
    
    # 인쇄 다이얼로그 차단 - 강화 버전
    BLOCK_PRINT_DIALOG = """
    (function() {
        // 1. window.print 완전히 무력화
        window.print = function() { 
            console.log('Print blocked');
            return false;
        };
        
        // 2. Object.defineProperty로 재정의 방지
        try {
            Object.defineProperty(window, 'print', {
                value: function() { console.log('Print blocked'); return false; },
                writable: false,
                configurable: false
            });
        } catch(e) {}
        
        // 3. 모든 print 관련 이벤트 차단
        ['beforeprint', 'afterprint'].forEach(function(eventType) {
            window.addEventListener(eventType, function(e) {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
                return false;
            }, true);
        });
        
        // 4. Ctrl+P 키 차단
        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
                e.preventDefault();
                e.stopPropagation();
                return false;
            }
        }, true);
        
        console.log('Print dialog blocking activated');
    })();
    """
    
    # 요소의 텍스트 내용 추출
    # {selector}: CSS 선택자
    GET_TEXT_CONTENT = """
    (function() {{
        var elem = document.querySelector('{selector}');
        return elem ? elem.textContent.trim() : null;
    }})()
    """
