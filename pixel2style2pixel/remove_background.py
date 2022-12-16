import cv2
import cvzone
import mediapipe as mp
from cvzone.SelfiSegmentationModule import SelfiSegmentation


segmentor = SelfiSegmentation()
img = cv2.imread('./output_source1/inference_results/mytargetimg0.png')

img_Out = segmentor.removeBG(img, (255,255,255), threshold=0.99)
cv2.imwrite('./output_source1/inference_results/rmbg_mytargetimg0.png',img_Out)