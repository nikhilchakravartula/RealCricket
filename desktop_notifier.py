from PyQt5 import Qt
import sys


class desktop_notifier:
    def __init__(self):
        self.app = Qt.QApplication(sys.argv)
        self.systemtray_icon = Qt.QSystemTrayIcon( Qt.QIcon('icon.jpg'))
        self.systemtray_icon.show()
        self.systemtray_icon.showMessage('Title', 'Content')

    def Notify(self, summary, message):
        self.systemtray_icon.showMessage('Title', 'Content')


