from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QSlider, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QSpinBox
from PyQt6.QtCore import Qt, QPoint, QRect

from Shared.Data import Data
from Shared.util.StylesManager import StyleType, getStyle
from Shared.util.Debugging import color_map, DebuggableQWidget

class GeneralControlWidget(DebuggableQWidget):
    def __init__(self, data: Data):
        super().__init__(data, 'debugCornerElement')
        self.data = data
        self.bgColor = color_map['darkWidgetBg']

        layout = QVBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # reset_view_button = QPushButton('Reset View')
        # reset_view_button.clicked.connect(self.onResetViewButtonClicked)
        # layout.addWidget(reset_view_button)

        self.x_pos = QLabel("X")
        self.y_pos = QLabel("Y")
        self.scale = QLabel("Scale")
        layout.addWidget(self.x_pos)
        layout.addWidget(self.y_pos)
        layout.addWidget(self.scale)

        self.data.movementListeners.append(self)
        self.update()

    def onMovement(self):
        self.x_pos.setText(f'X: {"{0:.2f}".format(self.data.navigation.globalPositionData.position[0])}')
        self.y_pos.setText(f'Y: {"{0:.2f}".format(self.data.navigation.globalPositionData.position[1])}')
        self.scale.setText(f'Scale: {"{0:.2f}".format(self.data.navigation.globalPositionData.scale)}')


class SpecialControlWidget(DebuggableQWidget):
    def __init__(self, data: Data):
        super().__init__(data, 'debugCornerElement')
        self.data = data
        self.bgColor = color_map['darkWidgetBg']

        layout = QVBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.update()


class TaskSpecificControls(DebuggableQWidget):
    def __init__(self, data: Data):
        super().__init__(data, 'debugCornerElement')
        self.data = data
        self.data.asteroidMenuWidget = self

        self.bgColor = color_map['darkWidgetBg']

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.update()


class LeftWidget(DebuggableQWidget):
    def __init__(self, data: Data):
        super().__init__(data, 'debugVbox')
        self.data = data

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        topWidget = GeneralControlWidget(data)
        bottomWidget = SpecialControlWidget(data)

        layout.addWidget(topWidget)
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)
        layout.addWidget(bottomWidget)

        topWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        bottomWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)


class RightWidget(DebuggableQWidget):
    def __init__(self, data: Data):
        super().__init__(data, 'debugVbox')
        self.data = data

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        layout.addWidget(TaskSpecificControls(data))
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)


class UIWidget(DebuggableQWidget):
    def __init__(self, data: Data):
        super().__init__(data, 'debugHBox')
        self.data = data
        self.ignoreMouse = False
        self.data.mainUi = self

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        leftWidget = LeftWidget(data)
        rightWidget = RightWidget(data)
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        leftWidget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        rightWidget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        layout.addWidget(leftWidget)
        layout.addItem(spacer)
        layout.addWidget(rightWidget)

    def isPosInsideOfRect(self, pos: QPoint, rect: QRect):
        return rect.contains(pos)
