import time

from Shared import Easings, Links


class ValueInterpolator:
    def __init__(self, defaultValue):
        self.defaultValue = defaultValue
        self.value = defaultValue
        self.instanceId = "Unknown"

        Links.globalData.animated.append(self)

        self.smoothValueStartTime = None
        self.smoothValueTarget = None
        self.smoothValueDuration = None
        self.smoothValueRealDuration = None
        self.smoothValueEasing = None
        self.alreadyBack = False
        self.twoWayAnimation = False
        self.realDurationCoef = None
        self.start_delay = 0

        self.customInternalGetFunc = None

    def setCustomInternalGetFunc(self, func):
        self.customInternalGetFunc = func

    def getValue(self):
        return self.value

    def getValueInt(self):
        return int(self.value)

    def setValue(self, value, stop=False):
        self.value = value
        if stop:
            self.stop()

    def stop(self):
        self.smoothValueStartTime = None

    def moveByValue(self, target_value, duration, start_delay=0, easingFunction=Easings.easeInOutQuad, realDurationCoef=0.2, fromLastTarget=True, easingFuncArgs=()):
        if not fromLastTarget:
            target_value = self.getValue() + target_value
        else:
            target_value = self.smoothValueTarget + target_value
        self.fadeToValue(target_value=target_value, duration=duration, start_delay=start_delay, easingFunction=easingFunction, realDurationCoef=realDurationCoef, easingFuncArgs=easingFuncArgs)

    def fadeToValue(self, target_value, duration, start_delay=0, easingFunction=Easings.easeInOutQuad, realDurationCoef=0.2, easingFuncArgs=()):
        self.alreadyBack = False
        self.twoWayAnimation = False

        self.initial_value = self.value
        self.start_delay = start_delay
        self.smoothValueStartTime = time.time()
        self.smoothValueTarget = target_value

        self.smoothValueDuration = duration
        self.smoothValueRealDuration = duration * min(1.0, realDurationCoef)
        self.realDurationCoef = realDurationCoef

        self.smoothValueEasing = easingFunction
        self.easingFuncArgs = easingFuncArgs

        self.perf_start_time = time.perf_counter()

    def pulseOutOfValue(self, target_value, duration, start_delay=0, easingFunction=Easings.easeInOutQuad, realDurationCoef=0.2, easingFuncArgs=()):
        value1 = target_value
        value2 = self.value
        self.value = value1
        self.fadeToValue(target_value=value2, duration=duration, start_delay=start_delay, easingFunction=easingFunction, realDurationCoef=realDurationCoef, easingFuncArgs=easingFuncArgs)

    def pulseToValue(self, target_value, duration, start_delay=0, easingFunction=Easings.easeInOutQuad, realDurationCoef=0.2, alreadyBack=False, easingFuncArgs=()):
        duration = duration / 2
        self.alreadyBack = alreadyBack
        self.twoWayAnimation = True

        self.initial_value = self.value
        self.start_delay = start_delay
        self.smoothValueStartTime = time.time()
        self.smoothValueTarget = target_value

        self.smoothValueDuration = duration
        self.smoothValueRealDuration = duration * min(1.0, realDurationCoef)
        self.realDurationCoef = realDurationCoef

        self.smoothValueEasing = easingFunction
        self.easingFuncArgs = easingFuncArgs

        self.perf_start_time = time.perf_counter()

    def animate(self):
        if self.smoothValueStartTime is not None:

            elapsedTime = time.time() - self.smoothValueStartTime - self.start_delay

            if elapsedTime < 0:
                return

            # print('Upd', '{0:.2f}'.format(elapsedTime), "/", '{0:.2f}'.format(self.smoothValueRealDuration))
            if elapsedTime >= self.smoothValueRealDuration:
                self.value = self.smoothValueTarget
                if self.alreadyBack or not self.twoWayAnimation:
                    self.smoothValueStartTime = None

                    self.perf_end_time = time.perf_counter()
                    elapsed_time = self.perf_end_time - self.perf_start_time
                    # if self.instanceId == 'mainNum2':
                    print(f"{self.instanceId} | Interpolator took {elapsed_time:.6f} seconds")
                else:
                    self.pulseToValue(target_value=self.defaultValue, duration=self.smoothValueDuration*2, realDurationCoef=self.realDurationCoef, easingFunction=self.smoothValueEasing, alreadyBack=True)
            else:
                # t = min(1.0, elapsedTime / self.smoothValueDuration)
                # t = self.smoothValueEasing(t)
                #
                # valueFrom = self.value
                # self.value = valueFrom + (self.smoothValueTarget - valueFrom) * t

                t = min(1.0, elapsedTime / self.smoothValueDuration)

                if self.easingFuncArgs is None:
                    t = self.smoothValueEasing(t)
                else:
                    t = self.smoothValueEasing(t, *self.easingFuncArgs)

                self.value = self.initial_value + (self.smoothValueTarget - self.initial_value) * t

                # if self.instanceId == 'mainNum2':
                print(self.instanceId, '|', 'value', self.value, '| time', elapsedTime, '/ totalTime', self.smoothValueDuration, '* realTimeCoef', self.realDurationCoef)
