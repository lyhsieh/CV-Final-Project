import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
import os.path as osp

segmentor = SelfiSegmentation()
path = './output_source2/inference_results'
save_path = './output_source_rmbg2'
if not osp.isdir(save_path):
    os.mkdir(save_path)
names = os.listdir(path)

for name in names:
    if 'mytargetimg' not in name:
        continue
    img = cv2.imread(osp.join(path,name))
    img_Out = segmentor.removeBG(img, (255,255,255), threshold=0.99)
    
    cv2.imwrite(osp.join(save_path,name),img_Out)