"""
Meteor Analysis System - IMX678
Main application entry point

Designer: Cubzilla470
Project: AstroBytes Meteor Analysis
Community: AstroBytes - https://www.facebook.com/groups/1400913928146353?locale=es_ES%2F
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MeteorAnalysisWindow

def main():
    """Initialize and run the Meteor Analysis application"""
    app = QApplication(sys.argv)
    window = MeteorAnalysisWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
