import RPi.GPIO as GPIO
#from picamera import PiCamera

from threading import Thread
import time
from datetime import datetime as DateTime


#---------------------------------------------------[ Globals ]--
# Modify as needed
GPIO_PIN = 7
INTERVAL = 5

# Leave as is
LAST_MOTION = time.monotonic() - INTERVAL
GUARDING = False
STOPPED = True


#-------------------------------------------------[ Functions ]--
def start_motion_detection(gpio_pin: int = GPIO_PIN):
    """Starts monitoring the motion sensor."""
    def _detect():
        """."""
        global GUARDING
        GUARDING = True

       # Setup PIR GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin, GPIO.IN)

        # Monitor
        STOPPED = False
        while GUARDING:
            if GPIO.input(gpio_pin):
                LAST_MOTION = time.monotonic()
            time.sleep(0.1)

    global GUARDING
    if GUARDING:
        print("Motion detection already running.")
    else:
        if STOPPED:
            print("Starting motion detection.")
            thread = Thread(target=_detect)
            thread.start()
        else:
            print("Wait for monitoring to stop first.")


def stop_motion_detection():
    """Stops monitoring the motion sensor GPIO pin."""
    global GUARDING
    if GUARDING:
        print("Stopping motion detection.")
        GUARDING = False
        while not STOPPED:
            time.sleep(0.5)
        print("Motion detection stopped.")


#------------------------------------------------------[ Main ]--
#camera = PiCamera()
start_motion_detection(GPIO_PIN)
try:
    while True:
        if (time.monotonic() - LAST_MOTION) <= INTERVAL:
            # take picture or record video for INTERVAL seconds or capture image
            time_stamp = DateTime.now().strftime("%Y%m%d-%H%M%S")
            #camera.capture(f"./img_{time_stamp}.jpg")
            print(f"{time_stamp} movement")
        time.sleep(INTERVAL)

except KeyboardInterrupt:
    stop_motion_detection()

print("Task failed successfully.")
