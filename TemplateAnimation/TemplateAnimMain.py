import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QResizeEvent, QMouseEvent, QKeyEvent
from PyQt6.QtWidgets import QApplication, QMainWindow

from Shared import Easings
from Shared.Data import Data
from Shared.util import StylesManager
from TemplateAnimation.Canvas import Canvas


class MainWindow(QMainWindow):
    def __init__(self, data: Data):
        super().__init__()
        self.data = data

        self.setWindowTitle("Task")
        self.setGeometry(100, 100, data.renderWindowSize[0], data.renderWindowSize[1])

        canvas = Canvas(data)
        self.setCentralWidget(canvas)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def resizeEvent(self, event: QResizeEvent):
        self.data.renderWindowSize = (event.size().width(), event.size().height())

    def wheelEvent(self, event):
        self.data.navigation.on_mousewheel(event)
        self.data.cameraMovement.stopSmoothAnimation()

    def isLeftClicked(self, event: QMouseEvent):
        return Qt.MouseButton.LeftButton in event.buttons()

    def isMiddleClicked(self, event: QMouseEvent):
        return Qt.MouseButton.MiddleButton in event.buttons()

    def mousePressEvent(self, event: QMouseEvent):
        if self.isMiddleClicked(event):
            pass
        elif self.isLeftClicked(event):
            self.data.navigation.on_mouse_click(event)
            self.data.cameraMovement.stopSmoothAnimation()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.data.navigation.on_mouse_release(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.isMiddleClicked(event):
            pass
        elif self.isLeftClicked(event):
            self.data.navigation.on_mouse_drag(event)

    def toggleFullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def keyReleaseEvent(self, event: QKeyEvent):
        if Qt.Key.Key_Return == event.key():
            data.cameraMovement.smoothMoveTo(targetX=100, targetY=0, targetScale=5, duration=5, realDurationCoef=0.2, easingFunction=Easings.easeInOutQuad)
        if Qt.Key.Key_Z == event.key():
            data.cameraSequences.perform_prev_sequence()
        if Qt.Key.Key_X == event.key():
            data.cameraSequences.perform_next_sequence()
        if Qt.Key.Key_F11 == event.key():
            self.toggleFullscreen()
        if Qt.Key.Key_U == event.key():
            data.hideUi = not data.hideUi
            for ui in data.uis:
                ui.setVisible(not data.hideUi)
                ui.repaint()


def load_style(file_path):
    with open(file_path, 'r') as file:
        return file.read()


if __name__ == "__main__":
    StylesManager.init()
    data = Data(fps=144, size=(1500, 800))

    app = QApplication(sys.argv)
    app.setStyleSheet(StylesManager.load_style('data/styles/style.css'))

    window = MainWindow(data)
    window.show()
    try:
        app.exec()
    except Exception as e:
        print(f"Exception: {e}")
