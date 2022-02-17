import tensorflow as tf
import cv2
import time
import argparse
import os
import math

import posenet

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=int, default=101)
parser.add_argument('--cam_id', type=int, default=0)
parser.add_argument('--cam_width', type=int, default=1280)
parser.add_argument('--cam_height', type=int, default=720)
parser.add_argument('--scale_factor', type=float, default=0.7125)
parser.add_argument('--file', type=str, default=None, help="Optionally use a video file instead of a live camera")
parser.add_argument('--output_dir', type=str, default='./savedimages')
args = parser.parse_args()

coord = []

def main():
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

            cv2.imshow('posenet', overlay_image)
            frame_count += 1

            # print("Results for image: ")
            # for pi in range(len(pose_scores)):
            #     if pose_scores[pi] == 0.:
            #         break
            #     print('Pose #%d, score = %f' % (pi, pose_scores[pi]))
            #     for ki, (s, c) in enumerate(zip(keypoint_scores[pi, :], keypoint_coords[pi, :, :])):
            #         if ki > 10 or (ki>4 and ki<7):
            #             print('Keypoint %s, score = %f, coord = %s' % (posenet.PART_NAMES[ki], s, c))
            #             score.append(s)
            #             coord.append(c)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if cv2.waitKey(1) & 0xFF == ord('a'):
                if pose_scores[0] <= 0.25:
                    print("Body not detected. Please try again.")
                else:    
                    img_name = "C:/Users/outan/OneDrive/Laptop/SHELL/PoseNet/savedimages/output.jpg"
                    cv2.imwrite(os.path.join(args.output_dir,'output.jpg'), overlay_image)
                    print("{} written!".format(img_name))
                    print()
                    print("Results for image: ")

                    print('Pose #%d, score = %f' % (0, pose_scores[0]))
                    for ki, (s, c) in enumerate(zip(keypoint_scores[0, :], keypoint_coords[0, :, :])):
                        if ki > 10 or (ki>4 and ki<7):
                            print('Keypoint %s, score = %f, coord = %s' % (posenet.PART_NAMES[ki], s, c))
                            coord.append(c)

                    print(coord)

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

                    bodyf = math.sqrt((lshoulder_x - rshoulder_x)**2 + (lshoulder_y - rshoulder_y)**2)
                    bodyc = math.sqrt((abs(2*rshoulder_x - lshoulder_x) - abs(2*rhip_x - lhip_x))**2 + (abs(2*rshoulder_y - lshoulder_y) - abs(2*rhip_y - lhip_y))**2)
                    # bodyc = abs(rshoulder_y - lshoulder_y) - abs(rhip_y - lhip_y)
                    bodyb_1 = math.sqrt((lhip_y - lknee_y)**2 + (lhip_x - lknee_x)**2)
                    bodyb_2 = math.sqrt((rhip_y - rknee_y)**2 + (rhip_x - rknee_x)**2)
                    bodyb = (bodyb_1+bodyb_2)/2
                    bodya_1 = math.sqrt((lknee_y - lankle_y)**2 + (lknee_x - lankle_x)**2)
                    bodya_2 = math.sqrt((rknee_y - rankle_y)**2 + (rknee_x - rankle_x)**2)
                    bodya = (bodya_1+bodya_2)/2

                    print('Length of\nA = %f\nB = %f\nC = %f\nF = %f' % (bodya, bodyb, bodyc, bodyf))


        print('Average FPS: ', frame_count / (time.time() - start))


if __name__ == "__main__":
    main()