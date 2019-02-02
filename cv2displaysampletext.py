import cv2
import numpy as np

img = np.zeros((512,512,3))

#define font properties

font = cv2.FONT_HERSHEY_SIMPLEX
displayat = (10,500) #start from first pixel, count from the topmost,leftmost and the first pixel
fontscale = 1
fontcolor = (255,255,255)
text = "Hello, World!"
linetype = 2

#merge text with img
cv2.putText(img,text,displayat,font,fontscale,fontcolor,linetype)

#display the image
cv2.imshow(text,img)
cv2.waitKey(0)
