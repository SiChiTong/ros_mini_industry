#! /usr/bin/env python
# coding=utf-8

import rospy
import sys
from sensor_msgs.msg import Image

from cv_bridge import CvBridge
import cv2

from detector import detector_main

from itheima_msgs.srv import GetBoxPoses, GetBoxPosesRequest, GetBoxPosesResponse
from itheima_msgs.msg import BoxPose

bridge = CvBridge()

rst_lst = None

def image_callback(msg):
    if not isinstance(msg, Image): return

    mat = bridge.imgmsg_to_cv2(msg, "bgr8")

    img = mat.copy()

    global rst_lst
    rst_lst = detector.start_find(img)

    # print("-----------", cv2.__version__, sys.version)
    half_mat = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    cv2.imshow("image", half_mat)
    cv2.waitKey(10)


def box_callback(req):
    while rst_lst is None:
        rospy.sleep(0.01)

    assembly_line_box_lst = rst_lst[0]
    agv_box_lst = rst_lst[1]

    #  line_poses: type 0是原料 1是成品
    #   agv_poses: type 0是原料 1是成品
    response = GetBoxPosesResponse()
    for item in assembly_line_box_lst:
        center = item[0]
        vector_x = item[1]
        type = item[2]

        pose = BoxPose()
        pose.center.append(center[0])
        pose.center.append(center[1])
        pose.vect.append(vector_x[0])
        pose.vect.append(vector_x[1])
        pose.type = type

        response.line_poses.append(pose)

    for item in agv_box_lst:
        center = item[0]
        vector_y = item[1]
        type = item[2]

        pose = BoxPose()
        pose.center.append(center[0])
        pose.center.append(center[1])
        pose.vect.append(vector_y[0])
        pose.vect.append(vector_y[1])
        pose.type = type

        response.agv_poses.append(pose)

    return response


if __name__ == '__main__':
    rospy.init_node("box_locator_node")

    subscriber = rospy.Subscriber("/kinect2/hd/image_color", Image, image_callback)

    service = rospy.Service("/box/poses", GetBoxPoses, box_callback)

    detector = detector_main.DetectorMain()


    rospy.spin()

    cv2.destroyAllWindows()
