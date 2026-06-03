"""
Main application window with tabbed interface
"""

import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QLabel, QPushButton, QStatusBar, 
                             QFileDialog, QMessageBox)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

from ui.tabs.setup_tab import SetupTab
from ui.tabs.player_tab import PlayerTab
from ui.tabs.analysis_tab import AnalysisTab
from ui.tabs.graphs_tab import GraphsTab
from config.config_manager import ConfigManager

class MeteorAnalysisWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meteor Analysis System - IMX678")
        self.setGeometry(100, 100, 1400, 900)
        
        # Configuration manager
        self.config_manager = ConfigManager()
        
        # Load application configuration
        self.load_config()
        
        # Initialize UI
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Create tabs
        self.setup_tab = SetupTab(self.config_manager)
        self.player_tab = PlayerTab()
        self.analysis_tab = AnalysisTab()
        self.graphs_tab = GraphsTab()
        
        # Add tabs to tab widget
        self.tabs.addTab(self.setup_tab, "Setup")
        self.tabs.addTab(self.player_tab, "Player")
        self.tabs.addTab(self.analysis_tab, "Analysis")
        self.tabs.addTab(self.graphs_tab, "Graphs")
        
        # Add tab widget to main layout
        main_layout.addWidget(self.tabs)
        
        # Create status bar
        self.statusBar().showMessage("Ready")
        
        # Create menu bar
        self.create_menu_bar()
        
        # Set application style
        self.setStyleSheet(self.get_stylesheet())
        
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        load_action = file_menu.addAction("Load Video")
        load_action.triggered.connect(self.load_video)
        
        save_config_action = file_menu.addAction("Save Configuration")
        save_config_action.triggered.connect(self.save_configuration)
        
        load_config_action = file_menu.addAction("Load Configuration")
        load_config_action.triggered.connect(self.load_configuration)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)
        
        credits_action = help_menu.addAction("Credits & Links")
        credits_action.triggered.connect(self.show_credits)
        
    def load_video(self):
        """Load a video file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load MP4 Video",
            "",
            "Video Files (*.mp4);;All Files (*)"
        )
        
        if file_path:
            self.setup_tab.set_video_path(file_path)
            self.player_tab.load_video(file_path)
            self.statusBar().showMessage(f"Loaded: {os.path.basename(file_path)}")
            
    def save_configuration(self):
        """Save current configuration"""
        config_data = {
            'video_path': self.player_tab.video_path if hasattr(self.player_tab, 'video_path') else '',
            'setup': self.setup_tab.get_config(),
            'analysis': self.analysis_tab.get_config(),
        }
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Configuration",
            "",
            "Config Files (*.cfg);;All Files (*)"
        )
        
        if file_path:
            self.config_manager.save_config(file_path, config_data)
            self.statusBar().showMessage(f"Configuration saved: {os.path.basename(file_path)}")
            
    def load_configuration(self):
        """Load a configuration file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Configuration",
            "",
            "Config Files (*.cfg);;All Files (*)"
        )
        
        if file_path:
            config_data = self.config_manager.load_config(file_path)
            if config_data:
                if 'video_path' in config_data and config_data['video_path']:
                    self.player_tab.load_video(config_data['video_path'])
                if 'setup' in config_data:
                    self.setup_tab.set_config(config_data['setup'])
                if 'analysis' in config_data:
                    self.analysis_tab.set_config(config_data['analysis'])
                self.statusBar().showMessage(f"Configuration loaded: {os.path.basename(file_path)}")
            
    def load_config(self):
        """Load application configuration from file"""
        config_data = self.config_manager.load_default_config()
        # Apply any saved window geometry or settings
        
    def show_about(self):
        """Show about dialog"""
        about_text = """
        <h2>Meteor Analysis System - IMX678</h2>
        <p>Professional meteor detection and analysis application</p>
        <p><b>Version:</b> 1.0.0</p>
        <p><b>Designer:</b> Cubzilla470</p>
        <p><b>Purpose:</b> Analyze meteor events from IMX678 camera footage</p>
        """
        QMessageBox.about(self, "About Meteor Analysis System", about_text)
        
    def show_credits(self):
        """Show credits and links dialog"""
        credits_text = """
        <h2>Credits & Links</h2>
        <p><b>Application Designer:</b> Cubzilla470</p>
        <p><b>Project:</b> AstroBytes Meteor Analysis System</p>
        <p><b>Community:</b> <a href="https://www.facebook.com/groups/1400913928146353?locale=es_ES%2F">
        AstroBytes Facebook Group</a></p>
        <p><b>Purpose:</b> Meteor detection and light curve analysis from IMX678 camera</p>
        <p><i>Bringing Meteors into Focus</i></p>
        """
        QMessageBox.information(self, "Credits & Links", credits_text)
        
    def get_stylesheet(self):
        """Return application stylesheet"""
        return """
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QTabWidget::pane {
            border: 1px solid #3d3d3d;
        }
        QTabBar::tab {
            background-color: #3d3d3d;
            color: #ffffff;
            padding: 8px 20px;
            border: 1px solid #2b2b2b;
        }
        QTabBar::tab:selected {
            background-color: #4a90e2;
            color: #ffffff;
        }
        QPushButton {
            background-color: #4a90e2;
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #357abd;
        }
        QPushButton:pressed {
            background-color: #2a5da3;
        }
        QLabel {
            color: #ffffff;
        }
        QLineEdit, QTextEdit, QComboBox {
            background-color: #3d3d3d;
            color: #ffffff;
            border: 1px solid #4a4a4a;
            padding: 5px;
            border-radius: 3px;
        }
        QStatusBar {
            background-color: #2b2b2b;
            color: #ffffff;
            border-top: 1px solid #3d3d3d;
        }
        QMenuBar {
            background-color: #2b2b2b;
            color: #ffffff;
            border-bottom: 1px solid #3d3d3d;
        }
        QMenuBar::item:selected {
            background-color: #4a90e2;
        }
        QMenu {
            background-color: #3d3d3d;
            color: #ffffff;
            border: 1px solid #4a4a4a;
        }
        QMenu::item:selected {
            background-color: #4a90e2;
        }
        """
