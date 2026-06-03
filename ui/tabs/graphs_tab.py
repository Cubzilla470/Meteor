"""
Graphs Tab - Light curve and motion analysis visualization
"""

import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QCheckBox, QSpinBox, QGroupBox, QFormLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class GraphsTab(QWidget):
    """Graphs and data visualization tab"""
    
    def __init__(self):
        super().__init__()
        self.zoom_level = 1.0
        self.event_center = 0
        self.init_ui()
        self.plot_demo_data()
        
    def init_ui(self):
        """Initialize the graphs tab UI"""
        layout = QVBoxLayout()
        
        title = QLabel("Light Curve & Motion Analysis")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        self.figure = Figure(figsize=(12, 8), dpi=100, facecolor='#2b2b2b')
        self.figure.patch.set_facecolor('#2b2b2b')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        zoom_group = QGroupBox("Zoom Controls")
        zoom_layout = QFormLayout()
        zoom_h_layout = QHBoxLayout()
        
        self.zoom_out_btn = QPushButton("Zoom Out")
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        zoom_h_layout.addWidget(self.zoom_out_btn)
        
        self.zoom_level_label = QLabel("Zoom: 1.0x")
        zoom_h_layout.addWidget(self.zoom_level_label)
        
        self.zoom_in_btn = QPushButton("Zoom In")
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        zoom_h_layout.addWidget(self.zoom_in_btn)
        
        self.reset_zoom_btn = QPushButton("Reset Zoom")
        self.reset_zoom_btn.clicked.connect(self.reset_zoom)
        zoom_h_layout.addWidget(self.reset_zoom_btn)
        
        zoom_layout.addRow("Zoom Control (Max 10x):", zoom_h_layout)
        
        self.zoom_spin = QSpinBox()
        self.zoom_spin.setRange(1, 10)
        self.zoom_spin.setValue(1)
        self.zoom_spin.setSuffix("x")
        self.zoom_spin.valueChanged.connect(self.on_zoom_spin_changed)
        zoom_layout.addRow("Direct Zoom:", self.zoom_spin)
        
        zoom_group.setLayout(zoom_layout)
        layout.addWidget(zoom_group)
        
        options_group = QGroupBox("Display Options")
        options_layout = QFormLayout()
        
        self.show_light_curve_check = QCheckBox("Show Light Curve")
        self.show_light_curve_check.setChecked(True)
        self.show_light_curve_check.stateChanged.connect(self.plot_demo_data)
        options_layout.addRow(self.show_light_curve_check)
        
        self.show_motion_check = QCheckBox("Show Motion Graph")
        self.show_motion_check.setChecked(True)
        self.show_motion_check.stateChanged.connect(self.plot_demo_data)
        options_layout.addRow(self.show_motion_check)
        
        self.show_confidence_check = QCheckBox("Show Confidence Band")
        self.show_confidence_check.setChecked(True)
        self.show_confidence_check.stateChanged.connect(self.plot_demo_data)
        options_layout.addRow(self.show_confidence_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        self.setLayout(layout)
        
    def plot_demo_data(self):
        """Plot demonstration data"""
        self.figure.clear()
        
        num_plots = 0
        if self.show_light_curve_check.isChecked():
            num_plots += 1
        if self.show_motion_check.isChecked():
            num_plots += 1
            
        if num_plots == 0:
            return
            
        frames = np.arange(0, 300)
        center = 150
        intensity = 30 * np.exp(-((frames - center) ** 2) / 200) + \
                   50 * np.exp(-np.maximum(0, frames - center) / 50)
        intensity = np.clip(intensity + np.random.normal(0, 2, len(frames)), 0, 255)
        
        if self.zoom_level > 1.0:
            zoom_center = self.event_center if self.event_center > 0 else center
            start_frame = max(0, int(zoom_center - 50 / self.zoom_level))
            end_frame = min(len(frames), int(zoom_center + 50 / self.zoom_level))
            frames = frames[start_frame:end_frame]
            intensity = intensity[start_frame:end_frame]
        
        if self.show_light_curve_check.isChecked():
            ax1 = self.figure.add_subplot(num_plots, 1, 1 if num_plots == 1 else 1)
            ax1.set_facecolor('#3d3d3d')
            ax1.grid(True, alpha=0.3, color='#666666')
            ax1.plot(frames, intensity, color='#4a90e2', linewidth=2, label='Light Intensity')
            ax1.fill_between(frames, intensity, alpha=0.3, color='#4a90e2')
            ax1.set_xlabel('Frame', color='#ffffff')
            ax1.set_ylabel('Intensity (0-255)', color='#ffffff')
            ax1.set_title('Light Curve Analysis', color='#ffffff', fontsize=12, fontweight='bold')
            ax1.tick_params(colors='#ffffff')
            ax1.legend(loc='upper right')
            
            if self.show_confidence_check.isChecked():
                confidence_band = intensity * 0.1
                ax1.fill_between(frames, intensity - confidence_band, intensity + confidence_band, 
                                alpha=0.2, color='#e2a54a', label='Confidence Band')
                ax1.legend(loc='upper right')
        
        if self.show_motion_check.isChecked():
            ax2 = self.figure.add_subplot(num_plots, 1, 2 if num_plots == 2 else 1)
            ax2.set_facecolor('#3d3d3d')
            ax2.grid(True, alpha=0.3, color='#666666')
            
            motion_x = 200 + 100 * np.sin(frames / 50) * intensity / 255
            motion_y = 200 + 80 * np.cos(frames / 40) * intensity / 255
            
            if self.zoom_level > 1.0:
                motion_x = motion_x[:len(frames)]
                motion_y = motion_y[:len(frames)]
            
            ax2.scatter(motion_x, motion_y, c=intensity, cmap='hot', s=30, alpha=0.7)
            ax2.set_xlabel('X Position (pixels)', color='#ffffff')
            ax2.set_ylabel('Y Position (pixels)', color='#ffffff')
            ax2.set_title('Motion Trajectory Analysis', color='#ffffff', fontsize=12, fontweight='bold')
            ax2.tick_params(colors='#ffffff')
            
            cbar = self.figure.colorbar(ax2.collections[0], ax=ax2)
            cbar.set_label('Intensity', color='#ffffff')
            cbar.ax.tick_params(colors='#ffffff')
        
        self.figure.tight_layout()
        self.canvas.draw()
        
    def zoom_in(self):
        """Zoom in on the graph"""
        if self.zoom_level < 10.0:
            self.zoom_level = min(10.0, self.zoom_level + 1.0)
            self.zoom_spin.blockSignals(True)
            self.zoom_spin.setValue(int(self.zoom_level))
            self.zoom_spin.blockSignals(False)
            self.zoom_level_label.setText(f"Zoom: {self.zoom_level:.1f}x")
            self.plot_demo_data()
            
    def zoom_out(self):
        """Zoom out on the graph"""
        if self.zoom_level > 1.0:
            self.zoom_level = max(1.0, self.zoom_level - 1.0)
            self.zoom_spin.blockSignals(True)
            self.zoom_spin.setValue(int(self.zoom_level))
            self.zoom_spin.blockSignals(False)
            self.zoom_level_label.setText(f"Zoom: {self.zoom_level:.1f}x")
            self.plot_demo_data()
            
    def reset_zoom(self):
        """Reset zoom to 1.0x"""
        self.zoom_level = 1.0
        self.zoom_spin.blockSignals(True)
        self.zoom_spin.setValue(1)
        self.zoom_spin.blockSignals(False)
        self.zoom_level_label.setText("Zoom: 1.0x")
        self.plot_demo_data()
        
    def on_zoom_spin_changed(self, value):
        """Handle zoom spin box change"""
        self.zoom_level = float(value)
        self.zoom_level_label.setText(f"Zoom: {self.zoom_level:.1f}x")
        self.plot_demo_data()
        
    def get_config(self):
        """Get current configuration"""
        return {
            'zoom_level': self.zoom_level,
            'show_light_curve': self.show_light_curve_check.isChecked(),
            'show_motion': self.show_motion_check.isChecked(),
            'show_confidence': self.show_confidence_check.isChecked(),
        }
        
    def set_config(self, config):
        """Set configuration from dictionary"""
        pass
