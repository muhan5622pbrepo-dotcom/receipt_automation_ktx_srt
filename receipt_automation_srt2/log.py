import datetime
import inspect
import os


def log(msg):
    """로그 출력: [시간] [파일명] [함수명] 메시지"""
    now = datetime.datetime.now().strftime("%H:%M:%S")
    frame = inspect.stack()[1]
    filename = os.path.basename(frame.filename)
    funcname = frame.function
    print(f"[{now}] [{filename}] [{funcname}] {msg}")
