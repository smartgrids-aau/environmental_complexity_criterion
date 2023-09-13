import glob
import cv2
import os
import numpy as np
os.chdir(os.path.dirname(os.path.realpath(__file__)))
names = glob.glob('*.png')
f = open('areas.csv','w')
for imgf in names:
    img = cv2.imread(imgf,0)
    w,h = np.shape(img)
    a = np.sum(img)/255
    f.write(imgf+","+str(int(a))+","+str(w*h)+","+str(a/(w*h))+"\n")
f.close()