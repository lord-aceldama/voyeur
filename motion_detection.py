# -*- coding: utf-8 -*-
""" A powerful feature of the Raspberry Pi is the row of GPIO (general-purpose input/output) pins along the top edge of
    the board. A 40-pin GPIO header is found on all current Raspberry Pi boards (unpopulated on Pi Zero and Pi Zero W).
    Prior to the Pi 1 Model B+ (2014), boards comprised a shorter 26-pin header.

    The full raspberry pi GPIO documentation can be found at https://www.raspberrypi.org/documentation/usage/gpio/
"""
__version__ = "0.9.0"
__author__ = "AceldamA"
__copyright__ = "AceldamA (C) 2021"
__credits__ = ["AceldamA"]
__license__ = "MIT"
__maintainer__ = "AceldamA"
__email__ = "aceldama@protonmail.com"
__status__ = "Development"

__all__ = ["GPIO_PIN", "MotionDetector"]

import sys
import time
from threading import Thread
from datetime import datetime as DateTime
try:
    import RPi.GPIO as GPIO
except ImportError:
    sys.exit("ERROR: Could not import RPi.GPIO.")


#==========================================================================================================[ GLOBALS ]==
# Modify as needed
GPIO_MODE = GPIO.BCM    #
GPIO_PIN = 7


#==================================================================================================[ MOTION DETECTOR ]==
class MotionDetector(Thread):
    """TODO: Docstring."""
    @property
    def gpio_pin(self) -> int:
        """TODO: Docstring."""
        return self._gpio

    @gpio_pin.setter
    def gpio_pin(self, value: int):
        """TODO: Pin number checking"""
        if value != self._gpio:
            self._gpio = value

    @property
    def running(self) -> bool:
        """TODO: Docstring."""
        return self._running

    @property
    def triggered(self) -> bool:
        """TODO: Docstring."""
        if self._triggered:
            self._triggered = False
            return True
        return False

    def __init__(self, gpio_pin: int):
        """TODO: Docstring."""
        # Init
        self._gpio: int = gpio_pin
        self._triggered = False
        self._stopping = False
        self._running = False

        # Inherit threading.thread
        super().__init__(target=self._detect)

    def _detect(self):
        """TODO: Docstring."""
        self._running = True

        try:
            # Setup PIR GPIO
            GPIO.setmode(GPIO_MODE)
            GPIO.setup(self._gpio, GPIO.IN)

            print("INFO: Motion detection started.")
            while not self._stopping:
                if not self._triggered:
                    self._triggered = GPIO.input(self.gpio_pin)
                    time.sleep(0.1)
        except:
            pass
        finally:
            # Setup PIR GPIO
            GPIO.cleanup()

        print("INFO: Motion detection stopped.")

    def start(self):
        """TODO: Docstring."""
        if self._running:
            print("FAIL: Motion detection already running.")
        else:
            super().__init__(target=self._detect)
            super().start()

    def stop(self):
        """TODO: Docstring."""
        if not self._running:
            print("FAIL: Motion detection not running.")
        else:
            if not self._stopping:
                print("INFO: Motion detection stopping.")
                self._stopping = True
            else:
                print("WARN: Already waiting for motion detection to stop.")


#==========================================================================================================[ TESTING ]==
def test():
    """TODO: Docstring."""
    try:
        while True:
            # take picture or record video for INTERVAL seconds or capture image
            time_stamp = DateTime.now().strftime("%Y%m%d-%H%M%S")
            # camera.capture(f"./img_{time_stamp}.jpg")
            print(f"{time_stamp} movement")

    except KeyboardInterrupt:
        stop_motion_detection()

    print("Task failed successfully.")


#=============================================================================================================[ MAIN ]==
if __name__ == "__main__":
    test()
