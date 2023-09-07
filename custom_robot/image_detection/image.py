#!/usr/bin/env python3

import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("image_topic_2",Image)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
      #rgb_image = cv2.imread(cv_image)
      gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
  
      binary_image = cv2.adaptiveThreshold(gray_image, 
                            255, 
                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                            cv2.THRESH_BINARY_INV, 5, 2)
      contours, hierarchy = cv2.findContours(binary_image.copy(), 
                                            cv2.RETR_EXTERNAL,
	                                        cv2.CHAIN_APPROX_SIMPLE)
      black_image = np.zeros([binary_image.shape[0], binary_image.shape[1],3],'uint8')
      for c in contours:
        area = cv2.contourArea(c)
        perimeter= cv2.arcLength(c, True)
        M = cv2.moments(c)
        cx=-1
        cy=-1
        if (M['m00']!=0):
          cx= int(M['m10']/M['m00'])
          cy= int(M['m01']/M['m00'])
        if (area>10):
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            cv2.drawContours(cv_image, [c], -1, (150,250,150), 1)
            cv2.drawContours(black_image, [c], -1, (150,250,150), 1)
            cv2.circle(black_image, (cx,cy),(int)(radius),(0,0,255),1)
            cv2.circle(cv_image, (cx,cy),(int)(radius),(0,0,255),1)
            cv2.putText(cv_image,"centroid",(cx - 25, cy - 25),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255, 255, 255), 2)  
            print(cx,cy)
    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = cv_image.shape
    if cols > 60 and rows > 60 :
      cv2.circle(cv_image, (50,50), 10, 255)

    cv2.imshow("Image window", cv_image)
    cv2.imshow("Black window", black_image)
    
    cv2.waitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)

