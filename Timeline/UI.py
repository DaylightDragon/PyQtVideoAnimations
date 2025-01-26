from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QSlider, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QSpinBox
from PyQt6.QtCore import Qt, QPoint, QRect

from Shared.Data import Data
from Shared.util.StylesManager import StyleType, getStyle
from Shared.util.Debugging import color_map, DebuggableQWidget

class CirculatingButtonSwitch(DebuggableQWidget):
    def __init__(self, data: Data, optionsList, onValueChange=None, buttonStyle=None):
        super().__init__(data, 'debugAdvancedNumberWidget')
        self.data = data
        self.optionsList = optionsList
        self.index = -1
        self.onValueChange = onValueChange

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.btn = QPushButton('a')
        self.btn.clicked.connect(self.onButtonClicked)

        if buttonStyle is not None:
            self.btn.setStyleSheet(buttonStyle)

        self.onButtonClicked()

        self.layout.addWidget(self.btn)

    def getButton(self):
        return self.btn

    def updateIndex(self):
        self.index += 1
        if self.index >= len(self.optionsList):
            self.index = 0

    def getIndex(self):
        return self.index

    def onButtonClicked(self):
        self.updateIndex()
        self.btn.setText(self.optionsList[self.index])
        if self.onValueChange is not None:
            self.onValueChange(self.index)


class AdvancedNumberWidget(DebuggableQWidget):
    def __init__(self, data: Data, name, range, default, onValueChange=None):
        super().__init__(data, 'debugAdvancedNumberWidget')
        self.data = data

        self.funcOnRelease = onValueChange
        self.name = name

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(range[0], range[1])
        self.slider.setValue(default)
        # self.slider.setSingleStep(20)
        # self.slider.setPageStep(20)
        self.slider.setTickPosition(QSlider.TickPosition.NoTicks)

        self.slider.valueChanged.connect(self.update_value)
        if self.funcOnRelease is not None:
            self.slider.valueChanged.connect(self.funcOnRelease)

        self.result_label = QLabel('', self)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.result_label)

        self.update_value(self.slider.value())
        # self.show()
        self.update()

    def getValue(self):
        return self.slider.value()

    def update_value(self, value):
        self.result_label.setText(f'{self.name}: {value}')


class AdvancedSpinboxWidget(DebuggableQWidget):
    def __init__(self, data: Data, name, range, default, onValueChange=None):
        super().__init__(data, 'debugAdvancedNumberWidget')
        self.data = data

        self.funcOnRelease = onValueChange
        self.name = name

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.spinbox = QSpinBox(self)
        self.spinbox.setRange(range[0], range[1])
        self.spinbox.setValue(default)

        self.spinbox.valueChanged.connect(self.update_value)
        if self.funcOnRelease is not None:
            self.spinbox.valueChanged.connect(self.funcOnRelease)

        self.result_label = QLabel('', self)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.spinbox)
        self.layout.addWidget(self.result_label)

        self.update_value(self.spinbox.value())
        # self.show()
        self.update()

    def getValue(self):
        return self.spinbox.value()

    def update_value(self, value):
        self.result_label.setText(f'{self.name}: {value}')


class GeneralControlWidget(DebuggableQWidget):
    def __init__(self, data: Data):
        super().__init__(data, 'debugCornerElement')
        self.data = data
        self.bgColor = color_map['darkWidgetBg']

        layout = QVBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.x_pos = QLabel("X")
        self.y_pos = QLabel("Y")
        self.scale = QLabel("Scale")
        layout.addWidget(self.x_pos)
        layout.addWidget(self.y_pos)
        layout.addWidget(self.scale)

        self.data.movementListeners.append(self)

        visualTitle = QLabel('Visual')
        visualTitle.setStyleSheet(getStyle(StyleType.SectionTitle))
        visualTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(visualTitle)

        self.fpsWidget = AdvancedNumberWidget(data=data, name="FPS", range=(1, 240), default=144, onValueChange=self.onFpsSliderRelease)
        layout.addWidget(self.fpsWidget)

        sensitivityTitle = QLabel('Sensitivity')
        sensitivityTitle.setStyleSheet(getStyle(StyleType.SectionTitle))
        sensitivityTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sensitivityTitle)

        self.movementSensitivityWidget = AdvancedNumberWidget(data=data, name="Movement", range=(-5, 10), default=0, onValueChange=self.onMovementSensitivityChange)
        layout.addWidget(self.movementSensitivityWidget)

        self.scalingSensitivityWidget = AdvancedNumberWidget(data=data, name="Scaling", range=(-5, 10), default=0, onValueChange=self.onScalingSensitivityChange)
        layout.addWidget(self.scalingSensitivityWidget)

    def onMovement(self):
        self.x_pos.setText(f'X: {"{0:.2f}".format(self.data.navigation.globalPositionData.position[0])}')
        self.y_pos.setText(f'Y: {"{0:.2f}".format(self.data.navigation.globalPositionData.position[1])}')
        self.scale.setText(f'Scale: {"{0:.2f}".format(self.data.navigation.globalPositionData.scale)}')

    def onFpsSliderRelease(self):
        self.data.frameUpdater.change_fps(self.fpsWidget.getValue())

    def onMovementSensitivityChange(self):
        self.data.mouseSensitivity = max(0, 1 + self.movementSensitivityWidget.getValue() / 5)

    def onScalingSensitivityChange(self):
        self.data.scrollSensitivity = max(0, 1 + self.scalingSensitivityWidget.getValue() / 5)

    def onResetViewButtonClicked(self):
        self.data.navigation.globalPositionData.position = (0, 0)
        self.data.navigation.globalPositionData.scale = 1

    def onResetSimulationButtonClicked(self):
        self.data.simulation.resetEverything()


class SpecialControlWidget(DebuggableQWidget):
    def __init__(self, data: Data):
        super().__init__(data, 'debugCornerElement')
        self.data = data
        self.bgColor = color_map['darkWidgetBg']

        layout = QVBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        title = QLabel('Inspect')
        title.setStyleSheet(getStyle(StyleType.SectionTitle))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        debugVisualsButton = QPushButton('Data')
        debugVisualsButton.clicked.connect(self.onDebugVisualsBtnClicked)

        debugButton = QPushButton('Layout')
        debugButton.clicked.connect(self.onDebugBtnClicked)

        layout.addWidget(debugVisualsButton)
        layout.addWidget(debugButton)

    def onDebugBtnClicked(self):
        self.data.debug = not self.data.debug

    def onDebugVisualsBtnClicked(self):
        pass


class TaskSpecificControls(DebuggableQWidget):
    def __init__(self, data: Data):
        super().__init__(data, 'debugCornerElement')
        self.data = data
        self.data.asteroidMenuWidget = self

        self.bgColor = color_map['darkWidgetBg']

        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel('Task Specific Tool')
        title.setStyleSheet(getStyle(StyleType.SectionTitle))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.spinboxValueWidget = AdvancedSpinboxWidget(data, 'Spinbox', (1, 400), 150, onValueChange=self.onSpinboxValueWidget)
        self.sliderValueWidget = AdvancedNumberWidget(data, 'Slider', (1, 400), 150, onValueChange=self.onSliderValueWidget)
        self.buttonWidget = QPushButton("Button")

        self.buttonWidget.clicked.connect(self.onButtonWidget)

        layout.addWidget(title)
        layout.addWidget(self.spinboxValueWidget)
        layout.addWidget(self.sliderValueWidget)
        layout.addWidget(self.buttonWidget)

        self.update()

    def onSpinboxValueWidget(self):
        pass

    def onSliderValueWidget(self):
        pass

    def onButtonWidget(self):
        pass


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
        # return (rect.x() <= pos.x() <= rect.x() + rect.width() and
        #         rect.y() <= pos.y() <= rect.y() + rect.height())
