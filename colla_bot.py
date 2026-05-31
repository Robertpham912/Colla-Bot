import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMenu, QAction
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QPoint

class CollaBot(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 1. THIẾT LẬP CỬA SỔ KHÔNG VIỀN & LUÔN NỔI TRÊN CÙNG
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground) 
        self.resize(160, 160) # Tăng nhẹ kích thước để chứa ảnh cho thoải mái
        
        # 2. LỚP NỀN KÍNH MỜ (SEMI-TRANSPARENT)
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, 160, 160)
        self.bg_label.setStyleSheet("""
            background-color: rgba(30, 41, 59, 0.85); 
            border: 3px solid #00f2ff;
            border-radius: 25px;
        """)
        
        # 3. NƠI HIỂN THỊ KHUÔN MẶT EMOJI
        self.avatar_label = QLabel(self)
        # Cho avatar nhỏ hơn lớp nền một chút (120x120) và nằm căn giữa (tọa độ x=20, y=20)
        self.avatar_label.setGeometry(20, 20, 120, 120)
        self.avatar_label.setScaledContents(True) # Tự động co giãn ảnh vừa khít khung
        
        # Cài đặt biểu cảm mặc định ban đầu là Bình thường
        self.set_mood("normal")

        self.old_pos = QPoint()

    # 4. HÀM ĐỔI CẢM XÚC CHO COLLA BOT
    def set_mood(self, mood):
        # Định nghĩa tên file tương ứng với từng cảm xúc
        mood_files = {
            "normal": "robot_normal.png",
            "happy": "robot_happy.png",
            "sad": "robot_sad.png",
            "sleep": "robot_sleep.png"
        }
        
        file_name = mood_files.get(mood, "robot_normal.png")
        
        # Kiểm tra xem file ảnh có tồn tại trong thư mục không trước khi nạp
        if os.path.exists(file_name):
            pixmap = QPixmap(file_name)
            self.avatar_label.setPixmap(pixmap)
            print(f"[Colla Bot] Đã đổi tâm trạng sang: {mood}")
        else:
            print(f"[Lỗi] Không tìm thấy file {file_name} trong thư mục!")

    # 5. LOGIC KÉO THẢ COLLA BOT
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if not self.old_pos.isNull():
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = QPoint()

    # 6. CLICK CHUỘT PHẢI ĐỂ HIỆN THANH CHỨC NĂNG & TEST CẢM XÚC
    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        contextMenu.setStyleSheet("""
            QMenu { background-color: rgba(15, 23, 42, 0.95); color: #f8fafc; border: 1px solid #334155; border-radius: 8px; padding: 4px; }
            QMenu::item { padding: 6px 20px; }
            QMenu::item:selected { background-color: #00f2ff; color: #0f172a; border-radius: 4px; }
        """)
        
        chat_action = QAction("💬 Chat với Colla Bot", self)
        
        # Thêm các nút test cảm xúc trực tiếp từ menu luôn cho tiện cậu ơi!
        happy_action = QAction("😀 Thử cảm xúc: Vui vẻ", self)
        sad_action = QAction("😢 Thử cảm xúc: Buồn", self)
        normal_action = QAction("🤖 Thử cảm xúc: Bình thường", self)
        
        sleep_action = QAction("💤 Đi ngủ", self)
        close_action = QAction("❌ Tắt Bot", self)
        
        # Kết nối các nút bấm với hàm set_mood
        happy_action.triggered.connect(lambda: self.set_mood("happy"))
        sad_action.triggered.connect(lambda: self.set_mood("sad"))
        normal_action.triggered.connect(lambda: self.set_mood("normal"))
        sleep_action.triggered.connect(lambda: self.set_mood("sleep"))
        close_action.triggered.connect(self.close)
        
        contextMenu.addAction(chat_action)
        contextMenu.addSeparator()
        contextMenu.addAction(normal_action)
        contextMenu.addAction(happy_action)
        contextMenu.addAction(sad_action)
        contextMenu.addAction(sleep_action)
        contextMenu.addSeparator()
        contextMenu.addAction(close_action)
        
        contextMenu.exec_(self.mapToGlobal(event.pos()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    bot = CollaBot()
    bot.show()
    sys.exit(app.exec_())
