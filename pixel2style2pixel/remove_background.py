import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
import os.path as osp
from PIL import Image
import numpy as np

segmentor = SelfiSegmentation()
path = './output_source2/inference_results'
save_path = './output_source_rmbg2'
if not osp.isdir(save_path):
    os.mkdir(save_path)
names = os.listdir(path)
names.remove('change.png')
# names.reverse()

for cnt,name in enumerate(names):
    
    img = np.asarray(Image.open(osp.join(path,name)))
    img_Out = segmentor.removeBG(img, (255,255,255), threshold=0.90)
    
    new_axis = np.zeros((*img_Out.shape[:-1],1),dtype='uint8')
    new_axis.fill(255)
    img_Out = np.concatenate((img_Out,new_axis),axis=2)
    
    for i in range(img_Out.shape[0]):
        for j in range(img_Out.shape[1]):
            if np.array_equal(img_Out[i][j],np.array([255,255,255,255])):
                img_Out[i][j] = np.array([255,255,255,0])
    
    Image.fromarray(img_Out[:960].astype('uint8')).save(osp.join(save_path,f'mytargetimg{cnt}.png'))
    # import pdb; pdb.set_trace()