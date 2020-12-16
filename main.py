import cv2
import time
import numpy as np
import argparse
import math


# calculates the angle between two vectors
def backAngle(a, b, x=(0, 0), y=(0, 1)):
    u = (a[0] - b[0], a[1] - b[1])
    v = (x[0] - y[0], x[1] - y[1])
    b = math.sqrt((u[0] * u[0] + u[1] * u[1]) * (v[0] * v[0] + v[1] * v[1]))
    t = u[0] * v[0] + u[1] * v[1]
    return math.degrees(math.acos(t / b))


def chackImg(frameinput):
    parser = argparse.ArgumentParser(description='Run keypoint detection')
    parser.add_argument("--device", default="cpu", help="Device to inference on")
    parser.add_argument("--image_file", default="netanelS.jpg", help="Input image")

    args = parser.parse_args()


    MODE = "COCO"

    if MODE == "COCO":
        protoFile = "pose/coco/pose_deploy_linevec.prototxt"
        weightsFile = "pose/coco/pose_iter_440000.caffemodel"
        nPoints = 4
        POSE_PAIRS = [[2, 8], [5, 11], [11, 12], [8, 9]]

    frame = cv2.imread(frameinput)
    frameCopy = np.copy(frame)
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    threshold = 0.1

    net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

    if args.device == "cpu":
        net.setPreferableBackend(cv2.dnn.DNN_TARGET_CPU)
        print("Using CPU device")
    elif args.device == "gpu":
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        print("Using GPU device")

    t = time.time()
    # input image dimensions for the network
    inWidth = 368
    inHeight = 368
    inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight),
                                (0, 0, 0), swapRB=False, crop=False)

    net.setInput(inpBlob)

    output = net.forward()
    print("time taken by network : {:.3f}".format(time.time() - t))

    H = output.shape[2]
    W = output.shape[3]

    # Empty list to store the detected keypoints
    points = []

    for i in range(nPoints):
    # confidence map of corresponding body's part.
        probMap = output[0, i, :, :]

        # Find global maxima of the probMap.
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

        # Scale the point to fit on the original image
        x = (frameWidth * point[0]) / W
        y = (frameHeight * point[1]) / H

        if prob > threshold:
            cv2.circle(frameCopy, (int(x), int(y)), 2, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
            cv2.putText(frameCopy, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1,
                        lineType=cv2.LINE_AA)

            # Add the point to the list if the probability is greater than the threshold
            points.append((int(x), int(y)))
            if i == 8:
                rhip = (x, y)
            if i == 2:
                rsho = (x, y)
            if i == 11:
                lhip = (x, y)
            if i == 5:
                lsho = (x, y)
        else:
            points.append(None)

    # Draw Skeleton
    for pair in POSE_PAIRS:
        partA = pair[0]
        partB = pair[1]

        if points[partA] and points[partB]:
            cv2.line(frame, points[partA], points[partB], (0, 255, 255), 2)
            cv2.circle(frame, points[partA], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)

    cv2.imshow('Output-Keypoints', frameCopy)
    cv2.imshow('Output-Skeleton', frame)

    cv2.imwrite('Output-Keypoints.jpg', frameCopy)
    cv2.imwrite('Output-Skeleton.jpg', frame)

    if points[8] and points[2]:
        rightAngle=backAngle(points[8], points[2])
        print("back angle (right): ", points[8], points[2], rightAngle)
    if points[11] and points[5]:
        leftAngle = backAngle(points[11], points[5])
        print("back angle (left): ", points[11], points[5], leftAngle)
    print("Total time taken : {:.3f}".format(time.time() - t))

    cv2.waitKey(0)
    return (rightAngle,leftAngle)




if __name__ == '__main__':

    print("YOU WIN!")