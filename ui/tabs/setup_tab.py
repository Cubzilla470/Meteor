"""
Setup Tab - Configuration management
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QSpinBox, QDoubleSpinBox,
                             QComboBox, QCheckBox, QGroupBox, QFormLayout,
                             QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SetupTab(QWidget):
    """Setup configuration tab"""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.video_path = ""
        self.init_ui()
        
    def init_ui(self):
        """Initialize the setup tab UI"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Meteor Analysis Setup")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Video Configuration Group
        video_group = QGroupBox("Video Configuration")
        video_layout = QFormLayout()
        
        self.video_path_input = QLineEdit()
        self.video_path_input.setReadOnly(True)
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_video)
        
        video_path_layout = QHBoxLayout()
        video_path_layout.addWidget(self.video_path_input)
        video_path_layout.addWidget(browse_btn)
        
        video_layout.addRow("Video File:", video_path_layout)
        video_group.setLayout(video_layout)
        layout.addWidget(video_group)
        
        # Analysis Parameters Group
        analysis_group = QGroupBox("Analysis Parameters")
        analysis_layout = QFormLayout()
        
        # Sensitivity
        self.sensitivity_spin = QDoubleSpinBox()
        self.sensitivity_spin.setRange(0.1, 10.0)
        self.sensitivity_spin.setValue(1.0)
        self.sensitivity_spin.setSingleStep(0.1)
        analysis_layout.addRow("Detection Sensitivity:", self.sensitivity_spin)
        
        # Minimum brightness threshold
        self.threshold_spin = QSpinBox()
        self.threshold_spin.setRange(0, 255)
        self.threshold_spin.setValue(50)
        analysis_layout.addRow("Brightness Threshold:", self.threshold_spin)
        
        # Minimum event duration
        self.duration_spin = QDoubleSpinBox()
        self.duration_spin.setRange(0.01, 10.0)
        self.duration_spin.setValue(0.1)
        self.duration_spin.setSingleStep(0.01)
        self.duration_spin.setSuffix(" seconds")
        analysis_layout.addRow("Min Event Duration:", self.duration_spin)
        
        analysis_group.setLayout(analysis_layout)
        layout.addWidget(analysis_group)
        
        # Classification Group
        classification_group = QGroupBox("Meteor Classification")
        classification_layout = QFormLayout()
        
        self.classification_combo = QComboBox()
        self.classification_combo.addItems([
            "All Types",
            "Fireball",
            "Fragmentation",
            "Ordinary",
            "Slow"
        ])
        classification_layout.addRow("Filter by Type:", self.classification_combo)
        
        self.confidence_check = QCheckBox("Show Confidence Percentage")
        self.confidence_check.setChecked(True)
        classification_layout.addRow(self.confidence_check)
        
        classification_group.setLayout(classification_layout)
        layout.addWidget(classification_group)
        
        # Display Options Group
        display_group = QGroupBox("Display Options")
        display_layout = QFormLayout()
        
        self.resizable_check = QCheckBox("Resizable Windows")
        self.resizable_check.setChecked(True)
        display_layout.addRow(self.resizable_check)
        
        self.dark_mode_check = QCheckBox("Dark Mode")
        self.dark_mode_check.setChecked(True)
        display_layout.addRow(self.dark_mode_check)
        
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)
        
        # Save/Reset buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save Configuration")
        save_btn.clicked.connect(self.save_configuration)
        button_layout.addWidget(save_btn)
        
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.clicked.connect(self.reset_defaults)
        button_layout.addWidget(reset_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
        
    def browse_video(self):
        """Browse for video file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select MP4 Video",
            "",
            "Video Files (*.mp4);;All Files (*)"
        )
        if file_path:
            self.set_video_path(file_path)
            
    def set_video_path(self, path):
        """Set video path"""
        self.video_path = path
        self.video_path_input.setText(path)
        
    def save_configuration(self):
        """Save current configuration"""
        config = self.get_config()
        QMessageBox.information(self, "Success", "Configuration saved successfully!")
        
    def reset_defaults(self):
        """Reset to default values"""
        self.sensitivity_spin.setValue(1.0)
        self.threshold_spin.setValue(50)
        self.duration_spin.setValue(0.1)
        self.classification_combo.setCurrentIndex(0)
        self.confidence_check.setChecked(True)
        self.resizable_check.setChecked(True)
        self.dark_mode_check.setChecked(True)
        QMessageBox.information(self, "Success", "Reset to defaults!")
        
    def get_config(self):
        """Get current configuration"""
        return {
            'video_path': self.video_path,
            'sensitivity': self.sensitivity_spin.value(),
            'threshold': self.threshold_spin.value(),
            'min_duration': self.duration_spin.value(),
            'classification_filter': self.classification_combo.currentText(),
            'show_confidence': self.confidence_check.isChecked(),
            'resizable_windows': self.resizable_check.isChecked(),
            'dark_mode': self.dark_mode_check.isChecked(),
        }
        
    def set_config(self, config):
        """Set configuration from dictionary"""
        if 'video_path' in config:
            self.set_video_path(config['video_path'])
        if 'sensitivity' in config:
            self.sensitivity_spin.setValue(config['sensitivity'])
        if 'threshold' in config:
            self.threshold_spin.setValue(config['threshold'])
        if 'min_duration' in config:
            self.duration_spin.setValue(config['min_duration'])
