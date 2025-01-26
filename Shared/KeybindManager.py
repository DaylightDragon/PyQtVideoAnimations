from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent


class KeybindManager:
    def __init__(self, data):
        self.data = data

    def keyReleaseEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Plus:
            self.data.navigation.zoomInSimple()
        if event.key() == Qt.Key.Key_Minus:
            self.data.navigation.zoomOutSimple()