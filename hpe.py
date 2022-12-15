import cv2
import mediapipe as mp
from time import sleep
from const import *
mp_drawing = mp.solutions.drawing_utils          # mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_pose = mp.solutions.pose                      # mediapipe pose estimation
import pdb
cap = cv2.VideoCapture(0)

# pose estimation action
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
        
    action1 = [False, False, False, False, False] # raise left hand, raise right hand, go left, go right, defense for left preson
    action2 = [False, False, False, False, False] # right person
    
    while True:
        ret, img = cap.read()
        if not ret:
            print("Cannot receive frame")
            break
        
        img = cv2.resize(img,(520,300))               # resize to accelarate the computing speed
        img = cv2.flip(img, 1)                     # flip right and left
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # turn BGR into RGB
        h, w, c = img.shape

        crop_img_1 = img[:, 0:int(w/2)]   # left side person
        crop_img_2 = img[:, int(w/2):w]   # right side person
        img.flags.writeable = False
        
        results_1 = pose.process(crop_img_1)        # get pose detection result
        if results_1.pose_landmarks is not None:
            for i in range(33):
                results_1.pose_landmarks.landmark[i].x /=2
                # print(f'person 1: {i} = {results_1.pose_landmarks.landmark[i].x}')
                left_hand_x, left_hand_y = results_1.pose_landmarks.landmark[15].x, results_1.pose_landmarks.landmark[15].y
                right_hand_x, right_hand_y = results_1.pose_landmarks.landmark[16].x, results_1.pose_landmarks.landmark[16].y
                nose_x, nose_y = results_1.pose_landmarks.landmark[0].x, results_1.pose_landmarks.landmark[0].y
                if left_hand_y < nose_y and action1[0] == False:
                    action1[0] = True
                    print('left person raising right hand')
                elif left_hand_y <= nose_y and action1[0] == True:
                    action1[0] = False
                elif right_hand_y < nose_y and action1[1] == False:
                    action1[1] = True
                    print('left person raising left hand')
                elif right_hand_y <= nose_y and action1[1] == True:
                    action1[1] = False
                elif nose_x - left_hand_x > 0.3 and action1[2] == False:  # this num hasn't been tested
                    action1[2] = True
                    print('left person punch left')
                # TODO : punch left restart
                elif right_hand_x - nose_x > 0.3 and action1[3] == False:  # this num hasn't been tested
                    action1[3] == True
                    print('left person punch right')
                # TODO : punch right restart
                elif abs(left_hand_x-right_hand_x) < 0.1 and action1[4] == False: # this num hasn't been tested
                    action1[4] == True
                    print('defense')
                # TODO : defense restart

                # else:
                #     print('L no action')
                
        results_2 = pose.process(crop_img_2)
        if results_2.pose_landmarks is not None:
            for i in range(33):
                results_2.pose_landmarks.landmark[i].x = (results_2.pose_landmarks.landmark[i].x)/2 + 0.5
                # print(f'person 2: {i} = {results_2.pose_landmarks.landmark[i].x}')
                left_hand_x, left_hand_y = results_2.pose_landmarks.landmark[15].x, results_2.pose_landmarks.landmark[15].y
                right_hand_x, right_hand_y = results_2.pose_landmarks.landmark[16].x, results_2.pose_landmarks.landmark[16].y
                nose_x, nose_y = results_2.pose_landmarks.landmark[0].x, results_2.pose_landmarks.landmark[0].y
                if left_hand_y < nose_y and action2[0] == False:
                    action2[0] = True
                    print('right person raising right hand')
                elif left_hand_y <= nose_y and action2[0] == True:
                    action2[0] = False
                elif right_hand_y < nose_y and action2[1] == False:
                    action2[1] = True
                    print('right person raising left hand')
                elif right_hand_y <= nose_y and action2[1] == True:
                    action2[1] = False
                elif nose_x - left_hand_x > 0.3 and action2[2] == False:  # this num hasn't been tested
                    action2[2] = True
                    print('right person punch left')
                # TODO : punch left restart
                elif right_hand_x - nose_x > 0.3 and action2[3] == False:  # this num hasn't been tested
                    action2[3] == True
                    print('right person punch right')
                # TODO : punch right restart
                elif abs(left_hand_x-right_hand_x) < 0.1 and action2[4] == False: # this num hasn't been tested
                    action2[4] == True
                    print('defense')
                # TODO : defense restart

        


        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        # according to pose detection result, label body nodes and skeleton
        mp_drawing.draw_landmarks(
            img,
            results_1.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        mp_drawing.draw_landmarks(
            img,
            results_2.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        cv2.imshow('oxxostudio', img)
        if cv2.waitKey(5) == ord('q'):
            break     # q to stop
cap.release()
cv2.destroyAllWindows()