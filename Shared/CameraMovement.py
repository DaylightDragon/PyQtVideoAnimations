import time

from Shared import Easings
from Shared.ValueInterpolator import ValueInterpolator


class CameraMovement:
    def __init__(self, data):
        self.data = data
        self.data.animated.append(self)
        # self.x = ValueInterpolator(0)
        # self.y = ValueInterpolator(0)
        # self.scale = ValueInterpolator(0)

        self.smoothMoveStartTime = None
        self.smoothMoveTargetX = 0
        self.smoothMoveTargetY = 0
        self.smoothMoveTargetScale = None
        self.smoothMoveDuration = None
        self.smoothMoveRealDuration = None
        self.smoothMoveEasing = None

    def getX(self):
        return self.data.navigation.globalPositionData.position[0]

    def getY(self):
        return self.data.navigation.globalPositionData.position[1]

    def getScale(self):
        return self.data.navigation.globalPositionData.scale

    def moveToX(self, x):
        self.data.navigation.globalPositionData.position = (x,
                                                            self.data.navigation.globalPositionData.position[1])

    def moveToY(self, y):
        self.data.navigation.globalPositionData.position = (self.data.navigation.globalPositionData.position[0],
                                                            y)

    def scaleTo(self, scale):
        self.data.navigation.globalPositionData.scale = scale

    def stopSmoothAnimation(self):
        self.smoothMoveStartTime = None

    def smoothMoveByXY(self, dTargetX, targetScale, duration, dTargetY=0, easingFunction=Easings.easeInOutQuad, realDurationCoef=0.2, fromLastTarget=True):
        if not fromLastTarget:
            dTargetX = self.getX() + dTargetX
            dTargetY = self.getY() + dTargetY
        else:
            dTargetX = self.smoothMoveTargetX + dTargetX
            dTargetY = self.smoothMoveTargetY + dTargetY
        self.smoothMoveTo(dTargetX, targetScale=targetScale, duration=duration, targetY=dTargetY, easingFunction=easingFunction, realDurationCoef=realDurationCoef)

    def smoothMoveTo(self, targetX, targetScale, duration, targetY=0,
                     easingFunction=Easings.easeInOutQuad, realDurationCoef=0.2):
        self.smoothMoveStartTime = time.time()
        self.smoothMoveTargetX = targetX
        self.smoothMoveTargetY = targetY
        self.smoothMoveTargetScale = targetScale

        self.smoothMoveDuration = duration
        self.smoothMoveRealDuration = duration * realDurationCoef

        self.smoothMoveEasing = easingFunction
        # print('Movement started')

    def animate(self):
        if self.smoothMoveStartTime is not None:
            elapsedTime = time.time() - self.smoothMoveStartTime

            # xLeft = self.getX() - self.smoothMoveTargetX
            # yLeft = self.getY() - self.smoothMoveTargetY

            # print('Upd', '{0:.2f}'.format(elapsedTime), "/", '{0:.2f}'.format(self.smoothMoveRealDuration))
            if elapsedTime >= self.smoothMoveRealDuration:
                self.moveToX(self.smoothMoveTargetX)
                self.moveToY(self.smoothMoveTargetY)
                self.scaleTo(self.smoothMoveTargetScale)
                self.smoothMoveStartTime = None
            else:
                t = min(1.0, elapsedTime / self.smoothMoveDuration)  # Нормализация времени
                t = self.smoothMoveEasing(t)  # Применение easing функции
                newX = self.getX() + (self.smoothMoveTargetX - self.getX()) * t
                newY = self.getY() + (self.smoothMoveTargetY - self.getY()) * t
                newScale = self.getScale() + (self.smoothMoveTargetScale - self.getScale()) * t
                self.moveToX(newX)
                self.moveToY(newY)
                self.scaleTo(newScale)

            try:
                self.data.navigation.notifyMovementListeners()
            except AttributeError:
                pass