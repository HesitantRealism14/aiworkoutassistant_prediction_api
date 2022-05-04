import aiworkout.poseDetector as pm
import cv2

def return_angle_squat(img):
    detector = pm.poseDetector()
    while True:
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img , False)
        if len(lmList) != 0:
            return detector.findAngle(img,12,24,26)


def return_angle_deadlift(img):
    detector = pm.poseDetector()
    while True:
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img , False)
        if len(lmList) != 0:
            return detector.findAngle(img,12,24,26)


def return_angle_bench(img):
    detector = pm.poseDetector()
    while True:
        #img = Image.open(img_file_buffer)
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img , False)
        if len(lmList) != 0:
            return detector.findAngle(img,16,14,12)

if __name__ == "__main__":
    print(return_angle_squat(cv2.imread('data/homesquat1.jpeg')))
