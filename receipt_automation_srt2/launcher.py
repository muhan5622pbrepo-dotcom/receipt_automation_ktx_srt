import sys
import json
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QDateEdit, QPushButton,
    QMessageBox, QFileDialog, QLineEdit
)
from PyQt6.QtCore import QDate, pyqtSignal, QObject, Qt
from PyQt6.QtGui import QFont
from config import Config


class WorkerSignals(QObject):
    """작업 완료 시그널"""
    finished_signal = pyqtSignal()
    start_signal = pyqtSignal(str, str, str)  # start_date, end_date, save_path


class SRTLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()
        self.signals.finished_signal.connect(self.on_finished)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("SRT 영수증 자동화")
        self.setGeometry(300, 300, 560, 340)
        self.setStyleSheet("background-color: #ffffff;")

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # ── 안내 문구 ──
        info_label = QLabel("브라우저가 열리면 로그인을 진행해주세요.")
        info_label.setFont(QFont("맑은 고딕", 11, QFont.Weight.Bold))
        info_label.setStyleSheet("""
            color: #1a73e8; 
            padding: 12px 16px;
            background-color: #e8f0fe;
            border-radius: 8px;
        """)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)

        # ── 조회 기간 ──
        date_label = QLabel("조회 기간")
        date_label.setFont(QFont("맑은 고딕", 10, QFont.Weight.Bold))
        date_label.setStyleSheet("color: #333; margin-top: 8px;")
        layout.addWidget(date_label)

        date_layout = QHBoxLayout()
        date_layout.setSpacing(12)

        start_label = QLabel("시작일")
        start_label.setFont(QFont("맑은 고딕", 9))
        start_label.setStyleSheet("color: #666;")
        
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addDays(-7))
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        self.start_date.setFixedHeight(36)
        self.start_date.setStyleSheet("""
            QDateEdit {
                padding: 6px 12px;
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: #fafafa;
                font-size: 10pt;
            }
            QDateEdit:focus {
                border: 1px solid #1a73e8;
                background-color: white;
            }
        """)

        end_label = QLabel("종료일")
        end_label.setFont(QFont("맑은 고딕", 9))
        end_label.setStyleSheet("color: #666;")
        
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setDisplayFormat("yyyy-MM-dd")
        self.end_date.setFixedHeight(36)
        self.end_date.setStyleSheet(self.start_date.styleSheet())

        date_layout.addWidget(start_label)
        date_layout.addWidget(self.start_date, 1)
        date_layout.addWidget(end_label)
        date_layout.addWidget(self.end_date, 1)
        layout.addLayout(date_layout)

        # ── 저장 경로 ──
        path_label = QLabel("저장 경로")
        path_label.setFont(QFont("맑은 고딕", 10, QFont.Weight.Bold))
        path_label.setStyleSheet("color: #333; margin-top: 8px;")
        layout.addWidget(path_label)

        path_layout = QHBoxLayout()
        path_layout.setSpacing(12)
        
        self.path_input = QLineEdit()
        self.path_input.setReadOnly(True)
        self.path_input.setText(Config.DEFAULT_SAVE_DIR)
        self.path_input.setFixedHeight(36)
        self.path_input.setStyleSheet("""
            QLineEdit {
                padding: 6px 12px;
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: #f5f5f5;
                color: #555;
                font-size: 9pt;
            }
        """)

        self.browse_btn = QPushButton("폴더 선택")
        self.browse_btn.setFixedHeight(36)
        self.browse_btn.setFixedWidth(100)
        self.browse_btn.setFont(QFont("맑은 고딕", 9))
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #333;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #e8e8e8;
                border: 1px solid #ccc;
            }
            QPushButton:pressed {
                background-color: #ddd;
            }
        """)
        self.browse_btn.clicked.connect(self.browse_folder)

        path_layout.addWidget(self.path_input, 1)
        path_layout.addWidget(self.browse_btn)
        layout.addLayout(path_layout)

        # 저장된 설정 로드
        self.load_settings()

        # Spacer
        layout.addSpacing(8)

        # ── 실행 버튼 ──
        self.start_btn = QPushButton("영수증 자동 저장")
        self.start_btn.setFixedHeight(48)
        self.start_btn.setFont(QFont("맑은 고딕", 12, QFont.Weight.Bold))
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #888;
            }
        """)
        self.start_btn.clicked.connect(self.start_automation)
        layout.addWidget(self.start_btn)

        self.setLayout(layout)

    # ── 설정 저장/로드 ──
    def load_settings(self):
        if os.path.exists(Config.SETTINGS_FILE):
            try:
                with open(Config.SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "save_path" in data:
                        self.path_input.setText(data["save_path"])
            except Exception:
                pass

    def save_settings(self):
        try:
            data = {"save_path": self.path_input.text()}
            with open(Config.SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "저장 폴더 선택")
        if folder:
            self.path_input.setText(folder)
            self.save_settings()

    # ── 작업 완료 ──
    def on_finished(self):
        self.start_btn.setEnabled(True)
        self.start_btn.setText("영수증 자동 저장")
        QMessageBox.information(self, "완료", "작업이 종료되었습니다.")

    # ── 자동화 시작 ──
    def start_automation(self):
        start_date = self.start_date.date().toString("yyyyMMdd")
        end_date = self.end_date.date().toString("yyyyMMdd")
        save_path = self.path_input.text()

        if not os.path.exists(save_path):
            try:
                os.makedirs(save_path)
            except Exception as e:
                QMessageBox.critical(self, "오류", f"저장 경로 생성 실패:\n{e}")
                return

        self.start_btn.setEnabled(False)
        self.start_btn.setText("작업 중...")

        # 시그널 발생 - main.py에서 처리
        self.signals.start_signal.emit(start_date, end_date, save_path)


if __name__ == "__main__":
    import main
    main.main()
