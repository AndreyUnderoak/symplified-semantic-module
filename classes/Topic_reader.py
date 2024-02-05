''' 
    This class provides reading the ros geo and image topics
    Made by Andrey Underoak(https://github.com/AndreyUnderoak) & Nancy Underoak(https://github.com/NancyUnderoak)
'''

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class Topic_reader():
   
    def __init__(self, img_topic):
        self.bridge = CvBridge()
        rospy.init_node('listener', anonymous=True)
        self.coor_subscriber = rospy.Subscriber(img_topic, Image, self.image_callback, queue_size=1)
        self.image_latest_message = 0

    def image_callback(self, message):
        self.image_latest_message = message
        
    def get_latest_image(self):
        if self.image_latest_message == 0:
            raise TopicException("No info from image topic")
        else:
            cv2_img = self.bridge.imgmsg_to_cv2(self.image_latest_message, "bgr8")
            return cv2_img
            
    
class TopicException(Exception):
    def __init__(self, message):
        self.message = message