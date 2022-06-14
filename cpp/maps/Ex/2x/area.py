import glob
import cv2
import os
import numpy as np
os.chdir(os.path.dirname(os.path.realpath(__file__)))
names = glob.glob('*.png')
ground_names = glob.glob('ground*.png')
grounds = []
for gf in ground_names:
    grounds.append(cv2.imread(gf,0))
names = list(set(names) - set(ground_names))
f = open('areas.csv','w')
for imgf in names:
    img = cv2.imread(imgf,0)
    w,h = np.shape(img)
    a = np.sum(img)/255
    index = 0
    for i in range(len(grounds)):
        if np.shape(img) == np.shape(grounds[i]):
            index = i
            break
    f.write(imgf.replace('.png','')+","+str(a/(w*h))+","+ground_names[i].replace('.png','')+"\n")
f.close()