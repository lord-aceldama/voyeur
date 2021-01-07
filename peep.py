from picamera import PiCamera
from .motion_detection import MotionDetector as MotionDetector

import time
from datetime import datetime as DateTime


#==========================================================================================================[ GLOBALS ]==
# Modify as needed
INTERVAL = 5


#==========================================================================================================[ TESTING ]==
def main():
    """TODO: Docstring."""
    camera = None
    try:
        camera = PiCamera()
    except:
        print("FAIL: Could not start the pi camera.")

    if camera:
        try:
            while True:
                pass
        except KeyboardInterrupt:
            pass

    print("Task failed successfully.")


#=============================================================================================================[ MAIN ]==
if __name__ == "__main__":
    main()
