import cv2
from torch_nano import *


def gstreamer_pipeline_in(capture_width=1280, capture_height=720, display_width=1280, display_height=720, framerate=60,
                          flip_method=0):
    """Gstreamer pipeline for capturing a CSI camera."""
    return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            #            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (capture_width, capture_height, framerate, flip_method)  # , display_width, display_height)
    )


def gstreamer_pipeline_out(width=640, height=480, framerate=30, ipaddr="127.0.0.1", port=5000):
    """Gstreamer pipeline for creating a network stream."""
    return (
        "appsrc ! "
        "video/x-raw, format=BGR ! "
        "queue ! "
        #        "framerate=(fraction)%d/1 ! "
        "videoconvert ! "
        "video/x-raw, format=BGRx ! "
        "nvvidconv ! "
        "omxh264enc ! "
        "video/x-h264, stream-format=byte-stream ! "
        #        "nvv4l2h264enc bitrate=16000000 insert-sps-pps=true ! "
        #        "video/x-raw, width=800, height=600 ! "
        #        "x264enc ! "
        "h264parse ! "
        #        "tune=zerolatency "
        #        "speed-preset=superfast ! "
        "rtph264pay pt=96 config-interval=1 ! "
        "udpsink host=192.168.0.110 port=5000 "
        #        "sync=false"
        #        % (framerate)
    )


def camera_nano():
    camera = cv2.VideoCapture(gstreamer_pipeline_in(flip_method=0), cv2.CAP_GSTREAMER)
    if camera.isOpened():

        out = cv2.VideoWriter(gstreamer_pipeline_out(), 0, 60, (1280, 720))

        # If VideoWriter isn't open then bail
        if not out.isOpened():
            print("VideoWriter not open! Abort!")
            exit(0)

        while out.isOpened:
            # Get frame
            ret, frame = camera.read()

            # TODO: What do we do with the results?
            res = torch_nano.run_inference(frame)
            print(res)

            # TODO : Test on your home network, it doesn't work with the gstreamer pipeline above.
            # out.write(res)

            #cv2.imshow("Camera", res)
            keyCode = cv2.waitKey(30) & 0xFF
            # Stop the program on the ESC key
            if keyCode == 27:
                break

        # Release resources
        camera.release()
        out.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera.")


if __name__ == "__main__":
    camera_nano()
