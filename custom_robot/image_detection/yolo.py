#!/usr/bin/env python3
import rospy
import cv2
import matplotlib.pyplot as plt
import numpy as np


#####reading the image######
image = cv2.imread("camera_image.jpeg")
print("image type = ", type(image))
print("image shape = ", image.shape)
#********************

#######just changed our colour to blue XD#########
new_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#cv2.imshow("new_image",new_image)
#cv2.waitKey(0)
#***************

########split the image##########
r,g,b = cv2.split(new_image)
print("r = ", r.shape)
print("g = ", g.shape)
print("b = ", b.shape)

new_image = cv2.merge((r,g,b))
#***********************

##########resizing the image###########

s = 10
w = int(new_image.shape[1]*s/100)
h = int(new_image.shape[1]*s/100)
dim = (w,h)
resize = cv2.resize(new_image, dim, interpolation = cv2.INTER_AREA)
print("after resizing = ",resize.shape)

#**************************

##########rotation of the image########
(h,w) = new_image.shape[:2]
c = (w/2 , h/2)
angle = 90
m = cv2.getRotationMatrix2D(c , angle, 1.0)
rotate = cv2.warpAffine(new_image , m , (h,w))
#cv2.imshow("new_image",rotate)
#cv2.waitKey(0)
#************************************


