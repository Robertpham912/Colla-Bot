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
import sys
import os
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QMenu, QAction, 
                             QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QPoint

# ==============================================================================
# 1. LỚP KHUNG CHAT (CHAT WINDOW)
# ==============================================================================
class ChatWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Thiết lập khung chat không viền và nằm trên cùng
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(300, 400) # Kích thước khung chat phù hợp góc màn hình

        # Giao diện kính mờ màu tối, đồng bộ với Colla Bot
        self.bg = QLabel(self)
        self.bg.setGeometry(0, 0, 300, 400)
        self.bg.setStyleSheet("""
            background-color: rgba(15, 23, 42, 0.9);
            border: 2px solid #334155;
            border-radius: 15px;
        """)

        # Bố cục giao diện bên trong (Layout)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        # Tiêu đề Khung Chat
        self.title_label = QLabel("💬 Colla Bot Chat", self)
        self.title_label.setStyleSheet("color: #00f2ff; font-weight: bold; font-size: 14px;")
        layout.addWidget(self.title_label)

        # Khung hiển thị nội dung cuộc trò chuyện (Lịch sử chat)
        self.chat_history = QTextEdit(self)
        self.chat_history.setReadOnly(True) # Người dùng không tự sửa nội dung ở đây được
        self.chat_history.setStyleSheet("""
            background-color: rgba(30, 41, 59, 0.5);
            color: #f8fafc;
            border: 1px solid #475569;
            border-radius: 8px;
            padding: 8px;
        """)
        self.chat_history.setFont(QFont("Arial", 10))
        layout.addWidget(self.chat_history)

        # Hàng nhập liệu (Ô text + Nút gửi)
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Nhập yêu cầu (Excel, Slide...)...")
        self.input_field.setStyleSheet("""
            background-color: #1e293b;
            color: #f8fafc;
            border: 1px solid #475569;
            border-radius: 6px;
            padding: 6px;
        """)
        self.input_field.returnPressed.connect(self.send_message) # Nhấn Enter để gửi
        input_layout.addWidget(self.input_field)

        self.send_btn = QPushButton("Gửi", self)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #00f2ff;
                color: #0f172a;
                font-weight: bold;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #38bdf8;
            }
        """)
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)

        layout.addLayout(input_layout)

        # Nút ẩn khung chat nhanh
        self.hide_btn = QPushButton("Thu gọn 🔼", self)
        self.hide_btn.setStyleSheet("color: #94a3b8; border: none; background: transparent; font-size: 11px;")
        self.hide_btn.clicked.connect(self.hide)
        layout.addWidget(self.hide_btn)

    def send_message(self):
        user_text = self.input_field.text().strip()
        if user_text:
            # Hiển thị tin nhắn của người dùng lên khung
            self.chat_history.append(f"<b>Cậu:</b> {user_text}")
            self.input_field.clear()
            
            # Giả lập phản hồi của Bot (Tạm thời trước khi gắn não Claude/Gemini)
            self.chat_history.append(f"<font color='#00f2ff'><b>Colla Bot:</b> Beep beep! Tớ đã nhận lệnh: '{user_text}'. Đang đợi cậu gắn não API vào nè!</font>")


# ==============================================================================
# 2. LỚP COLLA BOT CHÍNH (MAIN AVATAR)
# ==============================================================================
class CollaBot(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground) 
        self.resize(160, 160)
        
        # Nền kính mờ của Bot
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, 160, 160)
        self.bg_label.setStyleSheet("""
            background-color: rgba(30, 41, 59, 0.85); 
            border: 3px solid #00f2ff;
            border-radius: 25px;
        """)
        
        # Khuôn mặt Emoji
        self.avatar_label = QLabel(self)
        self.avatar_label.setGeometry(20, 20, 120, 120)
        self.avatar_label.setScaledContents(True)
        
        self.set_mood("normal")

        # KHỞI TẠO KHUNG CHAT ĐI KÈM
        self.chat_window = ChatWindow()
        
        self.old_pos = QPoint()
        self.is_moving = False # Biến kiểm tra xem người dùng đang kéo thả hay đang click

    def set_mood(self, mood):
        mood_files = {
            "normal": "robot_normal.png",
            "happy": "robot_happy.png",
            "sad": "robot_sad.png",
            "sleep": "robot_sleep.png"
        }
        file_name = mood_files.get(mood, "robot_normal.png")
        if os.path.exists(file_name):
            self.avatar_label.setPixmap(QPixmap(file_name))

    # XỬ LÝ CHUỘT KÉO THẢ VÀ CLICK
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()
            self.is_moving = False

    def mouseMoveEvent(self, event):
        if not self.old_pos.isNull():
            delta = QPoint(event.globalPos() - self.old_pos)
            # Nếu dịch chuyển chuột đi một khoảng đủ lớn, tính là đang kéo thả
            if delta.manhattanLength() > 5:
                self.is_moving = True
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.old_pos = event.globalPos()
                # Di chuyển khung chat đi theo Bot luôn cho dính nhau
                self.update_chat_position()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = QPoint()
            # NẾU CHỈ LÀ CLICK CHUỘT TRÁI (KHÔNG PHẢI KÉO THẢ) -> BUNG KHUNG CHAT
            if not self.is_moving:
                self.toggle_chat()

    def update_chat_position(self):
        # Đặt vị trí khung chat nằm ngay bên trái của Colla Bot
        self.chat_window.move(self.x() - 310, self.y() - 120)

    def toggle_chat(self):
        if self.chat_window.isVisible():
            self.chat_window.hide()
        else:
            self.update_chat_position()
            self.chat_window.show()

    # MENU CHUỘT PHẢI
    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        contextMenu.setStyleSheet("""
            QMenu { background-color: rgba(15, 23, 42, 0.95); color: #f8fafc; border: 1px solid #334155; border-radius: 8px; }
            QMenu::item { padding: 6px 20px; }
            QMenu::item:selected { background-color: #00f2ff; color: #0f172a; }
        """)
        
        happy_action = QAction("😀 Thử cảm xúc: Vui vẻ", self)
        sad_action = QAction("😢 Thử cảm xúc: Buồn", self)
        normal_action = QAction("🤖 Thử cảm xúc: Bình thường", self)
        close_action = QAction("❌ Tắt Bot", self)
        
        happy_action.triggered.connect(lambda: self.set_mood("happy"))
        sad_action.triggered.connect(lambda: self.set_mood("sad"))
        normal_action.triggered.connect(lambda: self.set_mood("normal"))
        close_action.triggered.connect(self.close)
        
        contextMenu.addAction(normal_action)
        contextMenu.addAction(happy_action)
        contextMenu.addAction(sad_action)
        contextMenu.addSeparator()
        contextMenu.addAction(close_action)
        contextMenu.exec_(self.mapToGlobal(event.pos()))

    def closeEvent(self, event):
        # Khi tắt Bot thì tắt luôn cả Khung chat ngầm đi kèm
        self.chat_window.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    bot = CollaBot()
    bot.show()
    sys.exit(app.exec_())
