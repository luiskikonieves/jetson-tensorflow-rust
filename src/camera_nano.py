import os
import time
import queue
import cv2
import numpy as np


def gstreamer_pipeline(capture_width=1280, capture_height=720, display_width=1280, display_height=720, framerate=60,
                       flip_method=0):
    return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (capture_width, capture_height, framerate, flip_method, display_width, display_height)
    )

def gstreamer_rtp(width=1280, height=720, framerate=60, flip_method=0):
    return (
        "appsrc ! "
        "videoconvert ! "
        "x264enc "
        "tune=zerolatency "
        "bitrate=500 "
        "speed-preset=superfast ! "
        "rtph264pay !"
        "udpsink host=127.0.0.1 port=5000"
        % (0, framerate, width, height, flip_method)
    )


def stream_video():
    camera = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if camera.isOpened():
        # Likely don't need this
        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)

        # Create the writer
        out = cv2.VideoWriter(gstreamer_rtp(flip_method=0))

        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
            # Get frame
            ret, frame = camera.read()
            # TODO: Update this to include object detection

            # TODO : Pipe the stream to network
            #out.write(frame)

            cv2.imshow("Camera", frame)
            keyCode = cv2.waitKey(30) & 0xFF
            # Stop the program on the ESC key
            if keyCode == 27:
                break
        camera.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    stream_video()
