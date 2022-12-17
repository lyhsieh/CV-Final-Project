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
        
    action1 = [False, False, False, False, False] # raise left hand, raise right hand, punch left, punch right, defense for left preson
    action2 = [False, False, False, False, False] # right person
    
    
    
    l_cnt, r_cnt = 0, 0

    while True:
        l_cnt += 1
        r_cnt += 1
        
        fighter_1 = [False,False,False,False,False]
        fighter_2 = [False,False,False,False,False]
        
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
            if l_cnt >= 5:
                l_cnt = 0
                # right person raising right hand
                if left_hand_y < nose_y and action1[0] == False:
                    action1[0], fighter_2[0] = True, True
                    print('right person raising right hand')
                    # l_cnt = 0
                elif left_hand_y >= nose_y and action1[0] == True:
                    action1[0] = False
                    print('None 0')
                        
                # right person raising left hand    
                elif right_hand_y < nose_y and action1[1] == False:
                    action1[1], fighter_2[1] = True, True
                    print('right person raising left hand')
                    # l_cnt = 0
                elif right_hand_y >= nose_y and action1[1] == True:
                    action1[1] = False
                    print('None 1')
                    
                # right person punch left    
                elif nose_x - left_hand_x > 0.3:  # this num hasn't been tested
                    if action1[2] == False:
                        action1[2], fighter_2[2] = True, True
                        print('right person punch left')
                    else:
                        print('action = punch left, but you should return to None')

                    # l_cnt = 0

                # right person punch right
                elif abs(right_hand_x - nose_x) > 0.5:  # this num hasn't been tested
                    if action1[3] == False:
                        action1[3], fighter_2[3] = True, True
                        print('right person punch right')
                    else:
                        print('action = punch right, but you should return to None')

                    # l_cnt = 0
                        
                # defense
                elif abs(left_hand_x - right_hand_x) < 0.1:  # this num hasn't been tested
                    if action1[4] == False:
                        action1[4], fighter_2[4] = True, True
                        print('defense')
                    else:
                        print('action = defense, but you should return to None')
                    
                # no action   
                else:
                    print('None')
                    action1[2], action1[3], action1[4] = False, False, False
                    # for i in range(len(action1)):
                    #     action1[i] = False
                
        results_2 = pose.process(crop_img_2)
        if results_2.pose_landmarks is not None:
            # print(abs(right_hand_x - nose_x))
            for i in range(33):
                results_2.pose_landmarks.landmark[i].x = (results_2.pose_landmarks.landmark[i].x)/2 + 0.5
                # print(f'person 2: {i} = {results_2.pose_landmarks.landmark[i].x}')
            left_hand_x, left_hand_y = results_2.pose_landmarks.landmark[15].x, results_2.pose_landmarks.landmark[15].y
            right_hand_x, right_hand_y = results_2.pose_landmarks.landmark[16].x, results_2.pose_landmarks.landmark[16].y
            nose_x, nose_y = results_2.pose_landmarks.landmark[0].x, results_2.pose_landmarks.landmark[0].y
            if r_cnt >= 5:
                r_cnt = 0
                # right person raising right hand
                if left_hand_y < nose_y and action2[0] == False:
                    action2[0], fighter_2[0] = True, True
                    print('right person raising right hand')
                    # r_cnt = 0
                elif left_hand_y >= nose_y and action2[0] == True:
                    action2[0] = False
                    print('None 0')
                        
                # right person raising left hand    
                elif right_hand_y < nose_y and action2[1] == False:
                    action2[1], fighter_2[1] = True, True
                    print('right person raising left hand')
                    # r_cnt = 0
                elif right_hand_y >= nose_y and action2[1] == True:
                    action2[1] = False
                    print('None 1')
                    
                # right person punch left    
                elif nose_x - left_hand_x > 0.3:  # this num hasn't been tested
                    if action2[2] == False:
                        action2[2], fighter_2[2] = True, True
                        print('right person punch left')
                    else:
                        print('action = punch left, but you should return to None')

                    # r_cnt = 0

                # right person punch right
                elif abs(right_hand_x - nose_x) > 0.5:  # this num hasn't been tested
                    if action2[3] == False:
                        action2[3], fighter_2[3] = True, True
                        print('right person punch right')
                    else:
                        print('action = punch right, but you should return to None')

                    # r_cnt = 0
                        
                # defense
                elif abs(left_hand_x - right_hand_x) < 0.1:  # this num hasn't been tested
                    if action2[4] == False:
                        action2[4], fighter_2[4] = True, True
                        print('defense')
                    else:
                        print('action = defense, but you should return to None')
                    
                # no action   
                else:
                    print('None')
                    action2[2], action2[3], action2[4] = False, False, False
                    # for i in range(len(action2)):
                    #     action2[i] = False
                        

        sleep(.1)

        


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