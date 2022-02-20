import tensorflow as tf
import cv2
import time
import argparse
import os
import math
import numpy as np
import serial
from object_detector import *

import posenet

# Load Aruco detector
parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=int, default=101)
parser.add_argument('--cam_id', type=int, default=2)
parser.add_argument('--cam_width', type=int, default=1280)
parser.add_argument('--cam_height', type=int, default=720)
parser.add_argument('--scale_factor', type=float, default=0.7125)
parser.add_argument('--file', type=str, default=None, help="Optionally use a video file instead of a live camera")
parser.add_argument('--output_dir', type=str, default='./savedimages')
args = parser.parse_args()

coord = []

def main():
    ser = serial.Serial('COM1', 9600)
    with tf.Session() as sess:
        model_cfg, model_outputs = posenet.load_model(args.model, sess)
        output_stride = model_cfg['output_stride']

        if args.file is not None:
            cap = cv2.VideoCapture(args.file)
        else:
            cap = cv2.VideoCapture(args.cam_id)
        cap.set(3, args.cam_width)
        cap.set(4, args.cam_height)

        start = time.time()
        frame_count = 0

        while True:
            input_image, display_image, output_scale = posenet.read_cap(
                cap, scale_factor=args.scale_factor, output_stride=output_stride)

            heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = sess.run(
                model_outputs,
                feed_dict={'image:0': input_image}
            )

            pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multi.decode_multiple_poses(
                heatmaps_result.squeeze(axis=0),
                offsets_result.squeeze(axis=0),
                displacement_fwd_result.squeeze(axis=0),
                displacement_bwd_result.squeeze(axis=0),
                output_stride=output_stride,
                max_pose_detections=10,
                min_pose_score=0.15)

            keypoint_coords *= output_scale

            # TODO this isn't particularly fast, use GL for drawing and display someday...
            overlay_image = posenet.draw_skel_and_kp(
                display_image, pose_scores, keypoint_scores, keypoint_coords,
                min_pose_score=0.15, min_part_score=0.1)

            # Get Aruco marker
            corners, _, _ = cv2.aruco.detectMarkers(display_image, aruco_dict, parameters=parameters)

            if corners:
                # Draw polygon around the marker
                int_corners = np.int0(corners)
                cv2.polylines(overlay_image, int_corners, True, (0, 255, 0), 5)

                # Aruco Perimeter
                aruco_perimeter = cv2.arcLength(corners[0], True)

                # Pixel to cm ratio
                pixel_cm_ratio = aruco_perimeter / 20

            cv2.imshow('Arjuna Team - Smart Seat', overlay_image)
            frame_count += 1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting program...")
                break
            if cv2.waitKey(1) & 0xFF == ord('a'):
                if pose_scores[0] <= 0.25:
                    print("Body not detected. Please try again.")
                elif corners:    
                    # img_name = "C:/Users/outan/OneDrive/Laptop/SHELL/PoseNet/savedimages/output.jpg"
                    cv2.imwrite(os.path.join(args.output_dir,'output.jpg'), overlay_image)
                    print("{} written!".format(os.path.join(args.output_dir,'output.jpg')))
                    print()
                    print("Results for image: ")

                    print('Pose #%d, score = %f' % (0, pose_scores[0]))
                    for ki, (s, c) in enumerate(zip(keypoint_scores[0, :], keypoint_coords[0, :, :])):
                        if ki > 10 or (ki>4 and ki<7):
                            print('Keypoint %s, score = %f, coord = %s' % (posenet.PART_NAMES[ki], s, c))
                            coord.append(c)

                    lshoulder_x     = coord[0][0]
                    lshoulder_y     = coord[0][1]
                    rshoulder_x     = coord[1][0]
                    rshoulder_y     = coord[1][1]
                    lhip_x          = coord[2][0]
                    lhip_y          = coord[2][1]
                    rhip_x          = coord[3][0]
                    rhip_y          = coord[3][1]
                    lknee_x         = coord[4][0]
                    lknee_y         = coord[4][1]
                    rknee_x         = coord[5][0]
                    rknee_y         = coord[5][1]
                    lankle_x        = coord[6][0]
                    lankle_y        = coord[6][1]
                    rankle_x        = coord[7][0]
                    rankle_y        = coord[7][1]

                    bodyf = (math.sqrt((lshoulder_x - rshoulder_x)**2 + (lshoulder_y - rshoulder_y)**2)) / pixel_cm_ratio
                    bodyc = (math.sqrt((abs(2*rshoulder_x - lshoulder_x) - abs(2*rhip_x - lhip_x))**2 + (abs(2*rshoulder_y - lshoulder_y) - abs(2*rhip_y - lhip_y))**2)) / pixel_cm_ratio
                    bodyb_1 = math.sqrt((lhip_y - lknee_y)**2 + (lhip_x - lknee_x)**2)
                    bodyb_2 = math.sqrt((rhip_y - rknee_y)**2 + (rhip_x - rknee_x)**2)
                    bodyb = ((bodyb_1+bodyb_2)/2) / pixel_cm_ratio
                    bodya_1 = math.sqrt((lknee_y - lankle_y)**2 + (lknee_x - lankle_x)**2)
                    bodya_2 = math.sqrt((rknee_y - rankle_y)**2 + (rknee_x - rankle_x)**2)
                    bodya = ((bodya_1+bodya_2)/2) / pixel_cm_ratio

                    print("Length of\nA = %f cm\nB = %f cm\nC = %f cm\nF = %fcm" % (bodya, bodyb, bodyc, bodyf))
                    data_send = "%d %d %d %d\r\n" % (int(bodya), int(bodyb), int(bodyc), int(bodyf))
                    ser.write(str.encode(data_send))
                    ser.close()
                else:
                    print("Marker not detected. Please try again.")


        print('Average FPS: ', frame_count / (time.time() - start))


if __name__ == "__main__":
    main()