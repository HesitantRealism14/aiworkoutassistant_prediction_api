import aiworkout.poseDetector as pm
import cv2

def return_angle_squat(img):
    detector = pm.poseDetector()
    score = 0
    while True:
        img_user = detector.findPose(img, False)
        lmList = detector.findPosition(img_user, False)
        if len(lmList) != 0:
            squat_mins = {}

            #head to hip
            squat_head_to_hip_right = detector.findAngle(img_user, 8, 12, 24)
            squat_head_to_hip_left = detector.findAngle(img_user, 7, 11, 23)
            if int(squat_head_to_hip_right) <= int(squat_head_to_hip_left):
                squat_mins['head_to_hip()'] = int(squat_head_to_hip_right)
            else:
                squat_mins['head_to_hip()'] = int(squat_head_to_hip_left)


            #hip to ankle
            squat_hip_to_ankle_right = detector.findAngle(img_user, 24, 26, 28)
            squat_hip_to_ankle_left = detector.findAngle(img_user, 23, 25, 27)
            if int(squat_hip_to_ankle_right) <= int(squat_hip_to_ankle_left):
                squat_mins['hip_to_ankle()'] = int(squat_hip_to_ankle_right)
            else:
                squat_mins['hip_to_ankle()'] = int(squat_hip_to_ankle_left)

            #shoulder to knee
            squat_shoulder_to_knee_right = detector.findAngle(img_user, 12, 24, 26)
            squat_shoulder_to_knee_left = detector.findAngle(img_user, 11, 23, 25)
            if int(squat_shoulder_to_knee_right) <= int(squat_shoulder_to_knee_left):
                squat_mins['shoulder_to_knee()'] = int(squat_shoulder_to_knee_right)
            else:
                squat_mins['shoulder_to_knee()'] = int(squat_shoulder_to_knee_left)


            #algorithm for squat
            if len(squat_mins) == 3:
                if squat_mins['hip_to_ankle()'] >= 170:
                    if squat_mins['head_to_hip()'] >=160:
                        score+=100
                        return f"score = {score} ==> nice squat! keep your core tighten"

                    else:
                        score-=50
                        return f"score = {score} ==> back straight up, tighten your abs!"

                else:
                    if squat_mins['shoulder_to_knee()'] <= 160:
                        score+=50
                        return f"score = {score} ==> back straight up,you are half way to 100!"

            else:
                return 'Unable to detect. Sorry.'

def return_angle_deadlift(img):
    detector = pm.poseDetector()
    score=0
    while True:
        img_user = detector.findPose(img, False)
        lmList = detector.findPosition(img , False)
        if len(lmList) != 0:
            deadlift_mins = {}
            #shoulder to ankle
            deadlift_shoulder_to_ankle_right = detector.findAngle(img_user, 12, 26, 28)
            deadlift_shoulder_to_ankle_left = detector.findAngle(img_user,  11, 25, 27)
            if int(deadlift_shoulder_to_ankle_right) <= int(deadlift_shoulder_to_ankle_left):
                deadlift_mins['shoulder_to_ankle()'] = int(deadlift_shoulder_to_ankle_right)
            else:
                deadlift_mins['shoulder_to_ankle()'] = int(deadlift_shoulder_to_ankle_left)

            #head_to_hip
            deadlift_head_to_hip_right = detector.findAngle(img_user, 8, 12, 24)
            deadlift_head_to_hip_left = detector.findAngle(img_user, 7, 11, 23)
            if int(deadlift_head_to_hip_right) <= int(deadlift_head_to_hip_left):
                deadlift_mins['head_to_hip()'] = int(deadlift_head_to_hip_right)
            else:
                deadlift_mins['head_to_hip()'] = int(deadlift_head_to_hip_left)

            #hip_to_ankle
            deadlift_hip_to_ankle_right = detector.findAngle(img_user, 24, 26, 28)
            deadlift_hip_to_ankle_left = detector.findAngle(img_user, 23, 25, 27)
            if int(deadlift_hip_to_ankle_right) <= int(deadlift_hip_to_ankle_left):
                deadlift_mins['hip_to_ankle()'] = int(deadlift_hip_to_ankle_right)
            else:
                deadlift_mins['hip_to_ankle()'] = int(deadlift_hip_to_ankle_left)

            #algorithm for deadlift
            if len(deadlift_mins) == 3:
                if deadlift_mins['hip_to_ankle()'] >= 170:
                    if deadlift_mins['head_to_hip()'] >=170:
                        score+=100
                        return f"score = {score} ==> nice squat! keep your core tighten"
                    else:
                        score-=50
                        return f"score = {score} ==> back straight up, tighten your abs!"
                else:
                    if deadlift_mins['shoulder_to_ankle()'] <= 170:
                        score+=50
                        return f"score = {score} ==> back straight up,you are half way to 100!"
            else:
                return 'Unable to detect. Sorry. '


def return_angle_bench(img):
    detector = pm.poseDetector()
    score=0
    while True:
        #img = Image.open(img_file_buffer)
        img_user = detector.findPose(img, False)
        lmList = detector.findPosition(img , False)
        if len(lmList) != 0:
            bench_mins = {}

            #arm to shoulder
            bench_arm_to_shoulder_right = detector.findAngle(img_user, 16, 14, 12)
            bench_arm_to_shoulder_left = detector.findAngle(img_user, 15, 13, 11)
            if int(bench_arm_to_shoulder_right) <= int(bench_arm_to_shoulder_left):
                bench_mins['arm_to_shoulder()'] = int(bench_arm_to_shoulder_right)
            else:
                bench_mins['arm_to_shoulder()'] = int(bench_arm_to_shoulder_left)

            #arm to hip
            bench_arm_to_hip_right = detector.findAngle(img_user, 14, 12, 24)
            bench_arm_to_hip_left = detector.findAngle(img_user, 13, 11, 23)
            if int(bench_arm_to_hip_right) <= int(bench_arm_to_hip_left):
                bench_mins['arm_to_hip()'] = int(bench_arm_to_hip_right)
            else:
                bench_mins['arm_to_hip()'] = int(bench_arm_to_hip_left)

            #shoulder to knee
            bench_shoulder_to_knee_right = detector.findAngle(img_user, 12, 24, 26)
            bench_shoulder_to_knee_left = detector.findAngle(img_user, 11, 23, 25)
            if int(bench_shoulder_to_knee_right) <= int(bench_shoulder_to_knee_left):
                bench_mins['shoulder_to_knee()'] = int(bench_shoulder_to_knee_right)
            else:
                bench_mins['shoulder_to_knee()'] = int(bench_shoulder_to_knee_left)

            #algorithm for bench
            if len(bench_mins) == 3:
                if bench_mins['arm_to_shoulder()'] >= 100:
                    if bench_mins['shoulder_to_knee()'] <=250:
                        score+=100
                        return f"score = {score} ==> nice bench press! keep your core tighten"
                    else:
                        score-=50
                        return f"score = {score} ==> tighten your abs,try to keep waist stick to seat"
                else:
                    if bench_mins['arm_to_hip()'] >= 200 or bench_mins['arm_to_hip()'] <=100:
                        score+=50
                        return f"score = {score} ==> tighten your abs,you are half way to 100!"
            else:
                return'Unable to detect. Sorry.'

if __name__ == "__main__":
    print(return_angle_squat(cv2.imread('data/homesquat1.jpeg')))
