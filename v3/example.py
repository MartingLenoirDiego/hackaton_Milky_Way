import cv2
import time
from gaze_tracking import GazeTracking

def eyet():
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)
    t1 = True
    left_pupil_t2 = (0,0)
    right_pupil_t2 = (0,0)
    calibration_pos = (0,0)
    while True:
        # We get a new frame from the webcam
        _, frame = webcam.read()

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""
        
        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()

        if (calibration_pos == (0,0) and left_pupil != None)  :
            time.sleep(2)
            calibration_pos = gaze.pupil_left_coords()
            print("calib " + str(calibration_pos))

        if t1 :
            left_pupil_t1 = gaze.pupil_left_coords()
            right_pupil_t1 = gaze.pupil_right_coords()
            left_pupil_t2 = (0,0)
            right_pupil_t2 = (0,0)
            t1 = False
        elif t1 == False :
            left_pupil_t2 = gaze.pupil_left_coords()
            right_pupil_t2 = gaze.pupil_right_coords()
            t1 = True
        
        if gaze.is_blinking():
            print("WINK")
        
        elif ((left_pupil_t1 != None) and (right_pupil_t1!= None) and (left_pupil_t2 != None) and (right_pupil_t2 != None)):
            position = (((left_pupil_t1[0] - calibration_pos[0])/float(calibration_pos[0]))*100)
            return position

