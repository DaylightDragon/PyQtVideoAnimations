from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtGui import QPainter, QColor

from Shared.Data import Data
from Shared.ColorInterpolator import ColorInterpolator
from Shared.NavigationUtils import Navigation
from Shared.FrameUpdater import FrameUpdater
from NumbersAnimation.UI import UIWidget
from NumbersAnimation.Simulation import Simulation


class Canvas(QWidget):
    def __init__(self, data: Data):
        super().__init__()
        self.data = data
        self.bgColor = ColorInterpolator(QColor("#222222"))

        self.data.canvas = self
        self.data.navigation = Navigation(self.data)
        self.data.frameUpdater = FrameUpdater(self.data)
        Simulation(self.data)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        ui = UIWidget(self.data)
        self.mainLayout.addWidget(ui)
        ui.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def update_physics(self):
        self.data.simulation.updatePhysics()

    def update_graphics(self):
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(self.rect(), self.bgColor.getValue())  # Background

        for animated in self.data.animated:
            animated.animate()
        self.data.simulation.updateGraphics(painter)  # Objects

        painter.end()
