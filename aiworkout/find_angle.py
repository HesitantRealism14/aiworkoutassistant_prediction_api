import aiworkout.poseDetector as pm
import cv2

#standard angles if angle > 180
def standardize(d):
    for k,v in d.items():
        if v > 180 :
            v_ = 360 -v
            d[k] = v_
        else:
            v = v
    return d

#output standardized angles
def check(d1,d2):
    if d1.values() == d2.values():
        return True
    else:
        return False

def return_angle_squat(img):
    detector = pm.poseDetector()
    score = 0
    while True:

        img_user = detector.findPose(img,False) # only draws the angles we detect
        lmList = detector.findPosition(img_user , draw=False)

        if len(lmList) != 0:

            squat_mins = {} #include all angles

            #head to hip
            squat_mins['squat_head_to_hip_right'] = round(detector.findAngle(img_user, 8, 12, 24),2)
            squat_mins['squat_head_to_hip_left'] = round(detector.findAngle(img_user, 7, 11, 23),2)

            #hip to ankle
            squat_mins['squat_hip_to_ankle_right'] = round(detector.findAngle(img_user, 24, 26, 28),2)
            squat_mins['squat_hip_to_ankle_left'] = round(detector.findAngle(img_user, 23, 25, 29),2)

            #shoulder to knee
            squat_mins['squat_hip_right'] = detector.findAngle(img_user, 26, 24, 23)
            squat_mins['squat_hip_left'] = detector.findAngle(img_user, 25, 23, 24)

            #algorithm for squat
            right_sum = squat_mins['squat_head_to_hip_right']+squat_mins['squat_hip_to_ankle_right']+squat_mins['squat_hip_right']
            left_sum = squat_mins['squat_head_to_hip_left']+squat_mins['squat_hip_to_ankle_left']+squat_mins['squat_hip_left']

            if abs(int(right_sum - left_sum)) <= 30:
                if abs(int(squat_mins['squat_head_to_hip_right'] - squat_mins['squat_head_to_hip_left'])) <=10:
                    score += 100
                    return f'score = {score} => Nice balance,keep your back straight and abs tight.'
                else:
                    score += 50
                    hh_right = squat_mins['squat_head_to_hip_right']
                    hh_left = squat_mins['squat_head_to_hip_left']
                    return f'score = {score} => IMBALANCE! Shoulder angles went wrong:right-{hh_right},left-{hh_left}. AI detected your shoulders are not parallel to ground.'
            else:
                score = score
                return f'score = {score} => A front picture would be better.Or a side picture to check your back.'

def return_angle_deadlift(img):
    detector = pm.poseDetector()
    score = 0
    while True:

        img_user = detector.findPose(img,False) # only draws the angles we detect
        lmList = detector.findPosition(img_user , draw=False)

        if len(lmList) != 0:

            deadlift_mins = {} #include all angles

            #head_to_hip
            deadlift_mins['deadlift_head_to_hip_right'] = round(detector.findAngle(img_user, 8, 12, 24),2)
            deadlift_mins['deadlift_head_to_hip_left'] = round(detector.findAngle(img_user, 7, 11, 23),2)

            #hip_to_ankle
            deadlift_mins['deadlift_hip_to_ankle_right'] = round(detector.findAngle(img_user, 24, 26, 28),2)
            deadlift_mins['deadlift_hip_to_ankle_left'] = round(detector.findAngle(img_user, 23, 25, 27),2)

            #head_to_ankle
            deadlift_mins['deadlift_head_to_ankle_right'] = round(detector.findAngle(img_user, 8, 24, 28),2)
            deadlift_mins['deadlift_head_to_ankle_left']= round(detector.findAngle(img_user, 7, 23, 27),2)

            #algorithm for deadlift
            right_sum = deadlift_mins['deadlift_head_to_hip_right']+deadlift_mins['deadlift_hip_to_ankle_right']
            left_sum = deadlift_mins['deadlift_head_to_hip_left']+deadlift_mins['deadlift_hip_to_ankle_left']

            #first step -> check balance
            if abs(int(right_sum - left_sum)) <= 30:

                #check a vital angle for the pose
                if deadlift_mins['deadlift_head_to_ankle_right'] > 150 and deadlift_mins['deadlift_head_to_ankle_right'] > 150:
                    score += 100
                    return f'score = {score} => Good job! Focus on your abs,keep your back straight and tighten your hip.'
                else:
                    score +=50
                    ha_right = deadlift_mins['deadlift_head_to_ankle_right']
                    ha_left = deadlift_mins['deadlift_head_to_ankle_right']
                    return f'score = {score} => Two angles went wrong: right-{ha_right},left-{ha_left} . Keep your back straight! Otherwise your waist and knees will be hurt!'

            #recommend user to upload a front picture
            else:
                score = score
                return f'score = {score} => A front picture would be better so that AI could detect your shoulders,hip and knees.'


def return_angle_bench(img):
    detector = pm.poseDetector()
    score = 0
    while True:

        img_user = detector.findPose(img,False) # only draws the angles we detect
        lmList = detector.findPosition(img_user , draw=False)

        if len(lmList) != 0:

            bench_mins = {}

            #arm to shoulder
            bench_mins['bench_arm_to_shoulder_right'] = round(detector.findAngle(img_user, 16, 14, 12),2)
            bench_mins['bench_arm_to_shoulder_left'] = round(detector.findAngle(img_user, 15, 13, 11),2)

            #arm to hip
            bench_mins['bench_arm_to_hip_right'] = round(detector.findAngle(img_user, 14, 12, 24),2)
            bench_mins['bench_arm_to_hip_left'] = round(detector.findAngle(img_user, 13, 11, 23),2)

            #shoulder to knee
            bench_mins['bench_shoulder_to_knee_right'] = round(detector.findAngle(img_user, 12, 24, 26),2)
            bench_mins['bench_shoulder_to_knee_left'] = round(detector.findAngle(img_user, 11, 23, 25),2)

            #algorithm for bench
            right_sum = bench_mins['bench_arm_to_hip_right']+bench_mins['bench_arm_to_shoulder_right']+bench_mins['bench_shoulder_to_knee_right']
            left_sum = bench_mins['bench_arm_to_hip_left']+bench_mins['bench_arm_to_shoulder_left']+bench_mins['bench_shoulder_to_knee_left']

            if abs(int(right_sum - left_sum)) <= 30:
                score += 100
                return f'score = {score} => Nice balance! Tighten your abs.'
            else:
                if bench_mins['bench_shoulder_to_knee_left'] > 150 and bench_mins['bench_shoulder_to_knee_right'] >150:
                    score += 50
                    return f'score = {score} => Good job! Keep your shoulder,hip and knee on the same line.Or you may hurt your waist.A front picture would allow AI to detect the balance of both sides.'
                else:
                    score = score
                    sk_right = bench_mins['bench_shoulder_to_knee_right']
                    sk_left = bench_mins['bench_shoulder_to_knee_left']
                    return f'score = {score} => Waist not stick to the seat or ground. Waist angles went wrong: right - {sk_right},left - {sk_left}.A front picture would allow AI to detect the balance of both sides.'


def return_angle_pushup(img): #pushup angles need standardization
    detector = pm.poseDetector()
    score = 0
    while True:

        img_user = detector.findPose(img,False) # only draws the angles we detect
        lmList = detector.findPosition(img_user , draw=False)

        if len(lmList) != 0:

            pushup_mins = {}

            #arm to shoulder
            pushup_mins['pushup_arm_to_shoulder_right'] = round(detector.findAngle(img_user, 16, 14, 12),2)
            pushup_mins['pushup_arm_to_shoulder_left'] = round(detector.findAngle(img_user, 15, 13, 11),2)

            #shoulder
            pushup_mins['pushup_shoulder_right'] = round(detector.findAngle(img_user, 14, 12, 11),2)
            pushup_mins['pushup_shoulder_left'] = round(detector.findAngle(img_user, 13, 11, 12),2)

            #head to ankle
            pushup_mins['pushup_head_to_ankle_right'] = round(detector.findAngle(img_user, 8, 24, 28),2)
            pushup_mins['pushup_head_to_ankle_left'] = round(detector.findAngle(img_user, 7, 23, 27),2)

            pushup_mins_ = standardize(pushup_mins)

            #algorithm for pushup
            right_sum = pushup_mins_['pushup_arm_to_shoulder_right']+pushup_mins_['pushup_shoulder_right']
            left_sum = pushup_mins_['pushup_arm_to_shoulder_left']+pushup_mins_['pushup_shoulder_left']

            if abs(int(right_sum - left_sum)) <= 30:
                score += 100
                return f'score = {score} => Good balance! Keep your back straight and your hip tighten downwards.Detection optimized.Here are your angles.{pushup_mins_}'
            else:
                if pushup_mins_['pushup_head_to_ankle_right'] > 160 and pushup_mins_['pushup_head_to_ankle_left'] > 160:
                    score += 50
                    return f'score = {score} => Good job! You kept your shoulder,hip and knee on the same line.A front picture would allow AI to detect the balance of both sides.'
                else:
                    score = score
                    ha_right = pushup_mins_['pushup_head_to_ankle_right']
                    ha_left = pushup_mins_['pushup_head_to_ankle_left']
                    return f'score = {score} => Body not parallel to ground. Hip angles went wrong: right - {ha_right}, left - {ha_left}.A front picture would allow AI to detect the balance of both sides.'


def return_angle_bridge(img):
    detector = pm.poseDetector()
    score = 0
    while True:

        img_user = detector.findPose(img,False) # only draws the angles we detect
        lmList = detector.findPosition(img_user , draw=False)

        if len(lmList) != 0:

            bridge_mins = {}

            #shoulder to knee
            bridge_mins['bridge_shoulder_to_knee_right'] = round(detector.findAngle(img_user, 12, 24, 26),2)
            bridge_mins['bridge_shoulder_to_knee_left'] = round(detector.findAngle(img_user, 11, 23, 25),2)

            #hip to ankle
            bridge_mins['bridge_hip_to_ankle_right'] = round(detector.findAngle(img_user, 24, 26, 28),2)
            bridge_mins['bridge_hip_to_ankle_left'] = round(detector.findAngle(img_user, 23, 25, 27),2)

            #knee to toe
            bridge_mins['bridge_knee_to_toe_right'] = round(detector.findAngle(img_user, 26, 28, 32),2)
            bridge_mins['bridge_knee_to_toe_left'] = round(detector.findAngle(img_user, 25, 27, 31),2)

            #hip
            bridge_mins['bridge_hip_right'] = round(detector.findAngle(img_user, 26, 24, 23),2)
            bridge_mins['bridge_hip_left'] = round(detector.findAngle(img_user, 25, 23, 24),2)

            #algorithm for hip bridge
            right_sum = bridge_mins['bridge_hip_to_ankle_right']+bridge_mins['bridge_knee_to_toe_right']+bridge_mins['bridge_shoulder_to_knee_right']
            left_sum = bridge_mins['bridge_hip_to_ankle_left']+bridge_mins['bridge_knee_to_toe_left']+bridge_mins['bridge_shoulder_to_knee_left']

            if abs(int(right_sum - left_sum)) <= 30:
                score += 100
                return f'score = {score} => Nice! Your shoulder,hip and knees are on the same line. Keep your abs and hips tighten.'

            else:
                if abs(int(bridge_mins['bridge_hip_left'] - bridge_mins['bridge_hip_right'])) < 100:
                    score += 50
                    return f'score = {score} => You balanced pretty well. Tighten your abs and hips or your waist and knees will be hurt.'

                else:
                    score = score
                    h_right = bridge_mins['bridge_hip_right']
                    h_left = bridge_mins['bridge_hip_left']
                    return f'score = {score} => Hip not parallel to ground. Hip angles went wrong:right - {h_right},left - {h_left}. A front picture would allow AI to detect the balance of both sides.'


if __name__ == "__main__":
    print(return_angle_squat(cv2.imread('data/homesquat1.jpeg')))
