"""
SRT 영수증 자동 저장 프로그램 v2
- nodriver 기반 브라우저 자동화
- PyQt6 UI
"""
import sys
import asyncio
import threading
import traceback
from PyQt6.QtWidgets import QApplication
from launcher import SRTLauncher
from srt_manager import SRTManager
from log import log


def run_automation(start_date, end_date, save_path, signals):
    """
    자동화 로직 실행 (별도 스레드)
    
    Args:
        start_date: yyyyMMdd 형식의 시작일
        end_date: yyyyMMdd 형식의 종료일
        save_path: 저장 경로
        signals: UI 시그널 객체
    """
    async def _run():
        manager = SRTManager()
        try:
            # 로그인 대기
            if await manager.wait_for_login():
                log("로그인 확인됨. 영수증 수집을 시작합니다.")
                
                # 날짜 설정
                log(f"조회 기간: {start_date} ~ {end_date}")
                await manager.set_date_range(start_date, end_date)
                log(f'1. 날짜 설정 완료')
                # 조회하기 버튼 클릭
                await manager.click_search_button()
                log(f'2. 조회하기 버튼 클릭 완료')
                # 영수증 캡처
                log(f"저장 경로: {save_path}")
                await manager.capture_receipts(save_path)
                log(f'3. 영수증 캡처 완료')
                
                # 로그인 성공 후 브라우저는 열어둔 채로 유지
                log("작업 완료. 브라우저는 열어둡니다.")
            else:
                log("로그인 실패 또는 중단됨.")
                # 로그인 실패 시에만 브라우저 닫기
                if manager:
                    await manager.close()
        except Exception as e:
            log(traceback.format_exc())
            # 에러 발생 시 브라우저 닫기
            if manager:
                await manager.close()
        finally:
            signals.finished_signal.emit()

    # 이벤트 루프 수동 관리 (CancelledError 방지)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(_run())
    except Exception:
        print(traceback.format_exc())
    finally:
        # 남은 태스크 정리
        try:
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()
            if pending:
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        except Exception:
            pass
        loop.close()


def main():
    """메인 함수 - UI 생성 및 시그널 연결"""
    app = QApplication(sys.argv)
    window = SRTLauncher()
    
    # start_signal 연결 - UI에서 시작 버튼 클릭 시 실행
    def on_start(start_date, end_date, save_path):
        t = threading.Thread(
            target=run_automation,
            args=(start_date, end_date, save_path, window.signals),
            daemon=True
        )
        t.start()
    
    window.signals.start_signal.connect(on_start)
    
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
