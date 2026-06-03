"""
Player Tab - Video playback and frame navigation
"""

import cv2
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QSlider, QSpinBox, QComboBox, QCheckBox)
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import QFrame

class VideoLabel(QFrame):
    """Custom QLabel for displaying video frames"""
    clicked = pyqtSignal(int, int)
    
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1a1a1a; border: 1px solid #3d3d3d;")
        self.pixmap = None
        
    def set_pixmap(self, pixmap):
        """Set the pixmap to display"""
        self.pixmap = pixmap
        self.update()
        
    def paintEvent(self, event):
        """Paint the video frame"""
        if self.pixmap:
            painter = __import__('PyQt5.QtGui', fromlist=['QPainter']).QPainter(self)
            x = (self.width() - self.pixmap.width()) // 2
            y = (self.height() - self.pixmap.height()) // 2
            painter.drawPixmap(x, y, self.pixmap)
            
    def mousePressEvent(self, event):
        """Handle mouse click for keyframe navigation"""
        self.clicked.emit(event.x(), event.y())

class PlayerTab(QWidget):
    """Video player tab"""
    
    def __init__(self):
        super().__init__()
        self.video_path = ""
        self.video_capture = None
        self.frame_count = 0
        self.current_frame = 0
        self.fps = 0
        self.is_playing = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the player tab UI"""
        layout = QVBoxLayout()
        
        title = QLabel("Video Player")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        self.video_display = VideoLabel()
        self.video_display.setMinimumHeight(600)
        self.video_display.clicked.connect(self.on_video_clicked)
        layout.addWidget(self.video_display)
        
        controls_layout = QHBoxLayout()
        
        self.play_btn = QPushButton("Play")
        self.play_btn.clicked.connect(self.toggle_play)
        controls_layout.addWidget(self.play_btn)
        
        stop_btn = QPushButton("Stop")
        stop_btn.clicked.connect(self.stop)
        controls_layout.addWidget(stop_btn)
        
        prev_btn = QPushButton("◄ Previous Frame")
        prev_btn.clicked.connect(self.prev_frame)
        controls_layout.addWidget(prev_btn)
        
        next_btn = QPushButton("Next Frame ►")
        next_btn.clicked.connect(self.next_frame_manual)
        controls_layout.addWidget(next_btn)
        
        layout.addLayout(controls_layout)
        
        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel("Current Frame:"))
        self.frame_label = QLabel("0")
        info_layout.addWidget(self.frame_label)
        info_layout.addWidget(QLabel("Total Frames:"))
        self.total_frames_label = QLabel("0")
        info_layout.addWidget(self.total_frames_label)
        info_layout.addWidget(QLabel("FPS:"))
        self.fps_label = QLabel("0")
        info_layout.addWidget(self.fps_label)
        info_layout.addStretch()
        layout.addLayout(info_layout)
        
        self.frame_slider = QSlider(Qt.Horizontal)
        self.frame_slider.setRange(0, 0)
        self.frame_slider.sliderMoved.connect(self.slider_moved)
        layout.addWidget(self.frame_slider)
        
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("Playback Speed:"))
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["0.5x", "1.0x", "1.5x", "2.0x"])
        self.speed_combo.setCurrentIndex(1)
        speed_layout.addWidget(self.speed_combo)
        speed_layout.addStretch()
        layout.addLayout(speed_layout)
        
        self.setLayout(layout)
        
    def load_video(self, video_path):
        """Load a video file"""
        if self.video_capture:
            self.video_capture.release()
        self.video_path = video_path
        self.video_capture = cv2.VideoCapture(video_path)
        
        if self.video_capture.isOpened():
            self.frame_count = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = self.video_capture.get(cv2.CAP_PROP_FPS)
            self.current_frame = 0
            self.frame_slider.setRange(0, self.frame_count - 1)
            self.total_frames_label.setText(str(self.frame_count))
            self.fps_label.setText(str(int(self.fps)))
            self.display_frame(0)
            
    def display_frame(self, frame_num):
        """Display a specific frame"""
        if not self.video_capture:
            return
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = self.video_capture.read()
        
        if ret:
            self.current_frame = frame_num
            self.frame_label.setText(str(frame_num))
            self.frame_slider.blockSignals(True)
            self.frame_slider.setValue(frame_num)
            self.frame_slider.blockSignals(False)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = 3 * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            scaled_pixmap = pixmap.scaledToWidth(800, Qt.SmoothTransformation)
            self.video_display.set_pixmap(scaled_pixmap)
            
    def toggle_play(self):
        """Toggle play/pause"""
        if self.is_playing:
            self.pause()
        else:
            self.play()
            
    def play(self):
        """Play video"""
        if not self.video_capture:
            return
        self.is_playing = True
        self.play_btn.setText("Pause")
        speed_text = self.speed_combo.currentText()
        speed = float(speed_text.replace('x', ''))
        interval = int(1000 / (self.fps * speed))
        self.timer.start(interval)
        
    def pause(self):
        """Pause video"""
        self.is_playing = False
        self.play_btn.setText("Play")
        self.timer.stop()
        
    def stop(self):
        """Stop video"""
        self.pause()
        self.display_frame(0)
        
    def next_frame(self):
        """Show next frame"""
        if self.current_frame < self.frame_count - 1:
            self.display_frame(self.current_frame + 1)
        else:
            self.pause()
            
    def next_frame_manual(self):
        """Show next frame"""
        if self.current_frame < self.frame_count - 1:
            self.display_frame(self.current_frame + 1)
            
    def prev_frame(self):
        """Show previous frame"""
        if self.current_frame > 0:
            self.display_frame(self.current_frame - 1)
            
    def slider_moved(self, value):
        """Handle slider movement"""
        self.pause()
        self.display_frame(value)
        
    def on_video_clicked(self, x, y):
        """Handle click on video display"""
        pass
