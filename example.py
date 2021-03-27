"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
import time
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
t1 = True
left_pupil_t2 = (0,0)
right_pupil_t2 = (0,0)
calibration_pos = (0,0)
"""def TimeOne():
    left_pupil_t1 = gaze.pupil_left_coords()
    right_pupil_t1 = gaze.pupil_right_coords()
    print(left_pupil_t1)
    time.sleep(2.0)
    print("Left x t2 = " + str(TimeTwo()[0][0]) + " Left x t1 = " + str(left_pupil_t1[0]))
    print(str(TimeTwo()[0][0]))
    #print(left_pupil_t1, TimeTwo()[0])

def TimeTwo():
    time.sleep(1.0)
    left_pupil_t2 = gaze.pupil_left_coords()
    right_pupil_t2 = gaze.pupil_right_coords()
    return left_pupil_t2, right_pupil_t2"""


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
        #print("t1 = " + str(left_pupil_t1) + " t2 = " + str(left_pupil_t2))
        t1 = False
    elif t1 == False :
        left_pupil_t2 = gaze.pupil_left_coords()
        right_pupil_t2 = gaze.pupil_right_coords()
        t1 = True
    
    if gaze.is_blinking():
        print("WINK")
    
    elif ((left_pupil_t1 != None) and (right_pupil_t1!= None) and (left_pupil_t2 != None) and (right_pupil_t2 != None)):
        position = (((left_pupil_t1[0] - calibration_pos[0])/float(calibration_pos[0]))*100)
        print("+  " + str(position) + " %")


    """elif ((left_pupil_t1 != None) and (right_pupil_t1!= None) and (left_pupil_t2 != None) and (right_pupil_t2 != None)):
        if ((((left_pupil_t1[0] - calibration_pos[0])/float(calibration_pos[0]))*100 >= 4) and left_pupil_t2 != (0,0) ):
            print("eye moving left!!")
            print(left_pupil_t1[0])
        elif ((((left_pupil_t1[0] - calibration_pos[0])/float(calibration_pos[0]))*100 <= -4) and left_pupil_t2 != (0,0) ):
            print("eye moving right!!")
            print(left_pupil_t1[0])
        elif ((((left_pupil_t1[0] - calibration_pos[0])/float(calibration_pos[0]))*100 > -4) and ((((left_pupil_t1[0] - calibration_pos[0])/float(calibration_pos[0]))*100 < 4) and left_pupil_t2 != (0,0) )):
            print("Not moving !!")
            print(left_pupil_t1[0])"""


    
    


    #if left_pupil_t1[0] - left_pupil_t2[0] > 0 :
     #   print("going right")
    
    """if gaze.is_blinking():
        text = "Blinking"
        print("blink" )
    elif gaze.is_right():
        text = "Looking right"
        print("right ", str(left_pupil[0]),   "  " , str(right_pupil[0]))
    elif gaze.is_left():
        text = "Looking left"
        print("left ", str(left_pupil[0]), "  " , str(right_pupil[0]))
    elif gaze.is_center():
        text = "Looking center"
        print("center ", str(left_pupil[0]), "  " , str(right_pupil[0]))"""
        

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break
