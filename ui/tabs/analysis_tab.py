"""
Analysis Tab - Meteor event detection and classification
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTextEdit, QComboBox, QListWidget, 
                             QListWidgetItem, QGroupBox, QFormLayout,
                             QProgressBar, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class AnalysisTab(QWidget):
    """Meteor analysis and classification tab"""
    
    def __init__(self):
        super().__init__()
        self.events = []
        self.current_event = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the analysis tab UI"""
        layout = QVBoxLayout()
        
        title = QLabel("Meteor Analysis & Classification")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        detection_group = QGroupBox("Event Detection")
        detection_layout = QHBoxLayout()
        
        analyze_btn = QPushButton("Analyze Video for Events")
        analyze_btn.clicked.connect(self.analyze_video)
        detection_layout.addWidget(analyze_btn)
        
        clear_btn = QPushButton("Clear Results")
        clear_btn.clicked.connect(self.clear_results)
        detection_layout.addWidget(clear_btn)
        
        detection_group.setLayout(detection_layout)
        layout.addWidget(detection_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        events_group = QGroupBox("Detected Events")
        events_layout = QVBoxLayout()
        
        self.events_list = QListWidget()
        self.events_list.itemClicked.connect(self.on_event_selected)
        events_layout.addWidget(self.events_list)
        events_group.setLayout(events_layout)
        layout.addWidget(events_group)
        
        details_group = QGroupBox("Event Details")
        details_layout = QFormLayout()
        
        self.event_type_label = QLabel("N/A")
        details_layout.addRow("Meteor Type:", self.event_type_label)
        
        self.confidence_label = QLabel("N/A")
        details_layout.addRow("Confidence:", self.confidence_label)
        
        self.start_frame_label = QLabel("N/A")
        details_layout.addRow("Start Frame:", self.start_frame_label)
        
        self.end_frame_label = QLabel("N/A")
        details_layout.addRow("End Frame:", self.end_frame_label)
        
        self.duration_label = QLabel("N/A")
        details_layout.addRow("Duration:", self.duration_label)
        
        self.brightness_label = QLabel("N/A")
        details_layout.addRow("Peak Brightness:", self.brightness_label)
        
        self.manual_type_combo = QComboBox()
        self.manual_type_combo.addItems([
            "Fireball - Very bright, slow decay",
            "Fragmentation - Multiple bright peaks",
            "Ordinary - Standard meteor",
            "Slow - Extended duration",
            "Bolide - Extremely bright explosion",
            "Sporadic - Unassociated meteor"
        ])
        details_layout.addRow("Manual Classification:", self.manual_type_combo)
        
        self.additional_info = QTextEdit()
        self.additional_info.setMaximumHeight(150)
        self.additional_info.setReadOnly(True)
        details_layout.addRow("Additional Info:", self.additional_info)
        
        details_group.setLayout(details_layout)
        layout.addWidget(details_group)
        
        action_layout = QHBoxLayout()
        
        save_event_btn = QPushButton("Save Event Analysis")
        save_event_btn.clicked.connect(self.save_event)
        action_layout.addWidget(save_event_btn)
        
        export_btn = QPushButton("Export Results")
        export_btn.clicked.connect(self.export_results)
        action_layout.addWidget(export_btn)
        
        layout.addLayout(action_layout)
        self.setLayout(layout)
        
    def analyze_video(self):
        """Analyze video for meteor events"""
        QMessageBox.information(
            self, 
            "Analysis",
            "Video analysis initiated.\n\nThis would process the video to detect meteor events,\nanalyze light curves, and classify meteor types.\n\n(Demo mode - simulating analysis)"
        )
        self.simulate_events()
        
    def simulate_events(self):
        """Simulate meteor event detection"""
        demo_events = [
            {
                'type': 'Fireball',
                'confidence': 94.5,
                'start_frame': 150,
                'end_frame': 245,
                'peak_brightness': 235,
                'duration': '3.2 seconds',
                'info': 'Very bright event with slow decay curve. Typical fireball characteristics.'
            },
            {
                'type': 'Fragmentation',
                'confidence': 87.2,
                'start_frame': 500,
                'end_frame': 620,
                'peak_brightness': 198,
                'duration': '4.0 seconds',
                'info': 'Multiple brightness peaks detected. Indicates fragmentation during atmospheric entry.'
            },
            {
                'type': 'Ordinary',
                'confidence': 91.3,
                'start_frame': 800,
                'end_frame': 870,
                'peak_brightness': 180,
                'duration': '2.8 seconds',
                'info': 'Standard meteor with typical light curve profile.'
            }
        ]
        
        self.events = demo_events
        self.refresh_events_list()
        
    def refresh_events_list(self):
        """Refresh the events list display"""
        self.events_list.clear()
        for i, event in enumerate(self.events):
            item_text = f"Event {i+1} - {event['type']} ({event['confidence']:.1f}%)"
            item = QListWidgetItem(item_text)
            self.events_list.addItem(item)
            
    def on_event_selected(self, item):
        """Handle event selection"""
        index = self.events_list.row(item)
        self.current_event = self.events[index]
        self.display_event_details()
        
    def display_event_details(self):
        """Display details of selected event"""
        if not self.current_event:
            return
        self.event_type_label.setText(self.current_event['type'])
        self.confidence_label.setText(f"{self.current_event['confidence']:.1f}%")
        self.start_frame_label.setText(str(self.current_event['start_frame']))
        self.end_frame_label.setText(str(self.current_event['end_frame']))
        self.duration_label.setText(self.current_event['duration'])
        self.brightness_label.setText(str(self.current_event['peak_brightness']))
        self.additional_info.setText(self.current_event['info'])
        
    def save_event(self):
        """Save current event analysis"""
        if self.current_event:
            QMessageBox.information(self, "Success", f"Event saved: {self.current_event['type']}")
        else:
            QMessageBox.warning(self, "No Event", "Please select an event first")
            
    def export_results(self):
        """Export analysis results"""
        QMessageBox.information(self, "Export", f"Exporting {len(self.events)} event(s) to CSV file...")
        
    def clear_results(self):
        """Clear all results"""
        self.events = []
        self.current_event = None
        self.refresh_events_list()
        self.event_type_label.setText("N/A")
        self.confidence_label.setText("N/A")
        self.start_frame_label.setText("N/A")
        self.end_frame_label.setText("N/A")
        self.duration_label.setText("N/A")
        self.brightness_label.setText("N/A")
        self.additional_info.setText("")
        
    def get_config(self):
        """Get current configuration"""
        return {'manual_type': self.manual_type_combo.currentText()}
        
    def set_config(self, config):
        """Set configuration from dictionary"""
        pass
