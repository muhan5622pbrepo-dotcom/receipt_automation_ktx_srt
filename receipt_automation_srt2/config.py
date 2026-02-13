import os

class Config:
    # URLs
    URL_LOGIN = "https://etk.srail.kr/cmc/01/selectLoginForm.do?pageId=TK0701000000"
    URL_RECEIPT_LIST = "https://etk.srail.kr/hpg/hta/03/selectBreakdownList.do?pageId=TK0102030100"
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DEFAULT_SAVE_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "출장복명")
    SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
    
    # Browser Profile - persistent profile for "회원 아이디 저장" support
    PROFILE_DIR = os.path.join(os.environ.get("TEMP", "."), "srt_chrome_profile_v2")
