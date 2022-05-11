
import cv2
import aiworkout.poseDetector as pm


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

def return_angle_squat_cn(img):
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
                    if abs(int(squat_mins['squat_hip_right'] - squat_mins['squat_hip_left'])) <= 10:
                        if abs(int(squat_mins['squat_hip_to_ankle_right'] - squat_mins['squat_hip_to_ankle_left'])) <= 10:
                            score += 100
                            return f'分数 = {score} => 动作标准!站立时保持肩臀膝三点一线.收紧腹部核心.夹紧臀部肌肉.'
                        else:
                            score += 50
                            ha_right = squat_mins['squat_hip_to_ankle_right']
                            ha_left = squat_mins['squat_hip_to_ankle_left']
                            return f'分数 = {score} => 双膝不平衡! 两膝角度 : 右 - {ha_right},左 - {ha_left} . 膝盖不可超过脚尖.挺直背部.收紧腹部核心.'
                    else:
                        score += 30
                        h_right = squat_mins['squat_hip_right']
                        h_left = squat_mins['squat_hip_left']
                        return f'分数 = {score} => 臀部不平衡! 臀部角度 : 右 - {h_right},左 - {h_left} . 向后推臀.背部挺直.收紧腹部核心.'

                else:
                    score += 30
                    hh_right = squat_mins['squat_head_to_hip_right']
                    hh_left = squat_mins['squat_head_to_hip_left']
                    return f'分数 = {score} => 双肩不平衡! 双肩角度 : 右 - {hh_right},左 - {hh_left}. 肩膀需与地面保持平行.'
            else:
                score = score
                return '角度测算偏差过大.正面照片可以帮助我们对您的动作进行精确分析.'

def return_angle_deadlift_cn(img):
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
            right_sum = deadlift_mins['deadlift_head_to_hip_right']+deadlift_mins['deadlift_hip_to_ankle_right']+deadlift_mins['deadlift_head_to_ankle_right']
            left_sum = deadlift_mins['deadlift_head_to_hip_left']+deadlift_mins['deadlift_hip_to_ankle_left']+deadlift_mins['deadlift_head_to_ankle_left']

            #first step -> check balance
            if abs(int(right_sum - left_sum)) <= 30:
                if abs(int(deadlift_mins['deadlift_hip_to_ankle_right'] - deadlift_mins['deadlift_hip_to_ankle_left'])) <=10:
                    if abs(int(deadlift_mins['deadlift_head_to_ankle_right'] - deadlift_mins['deadlift_head_to_ankle_left'])) <=10:
                        if abs(int(deadlift_mins['deadlift_head_to_hip_right'] - deadlift_mins['deadlift_head_to_hip_left'])) <= 10:
                            score += 100
                            return f'分数 = {score} => 动作标准! 注意收紧腹部核心. 挺直背部. 夹紧臀部.'
                        else:
                            score +=50
                            hh_right = deadlift_mins['deadlift_head_to_hip_right']
                            hh_left = deadlift_mins['deadlift_head_to_hip_left']
                            return f'分数 = {score} => 双肩不平衡! 双肩角度 : 右 - {hh_right}, 左 - {hh_left} . 双肩需与地面平行.挺直背部. 收紧腹部核心. 避免伤及腰部和膝盖.'
                    else:
                        score += 30
                        ha_right = deadlift_mins['deadlift_head_to_ankle_right']
                        ha_left = deadlift_mins['deadlift_head_to_ankle_left']
                        return f'分数 = {score} => 臀部不平衡! 臀部角度 : 右 - {ha_right}, 左 - {ha_left} . 起身时夹紧臀部肌肉. 站姿状态下肩臀膝三点一线. 挺直背部.收紧腹部核心.'
                else:
                    score += 50
                    hipa_right = deadlift_mins['deadlift_hip_to_ankle_right']
                    hipa_left = deadlift_mins['deadlift_hip_to_ankle_left']
                    return f'分数 = {score} => 双膝不平衡! 双膝角度 : 右 - {hipa_right},左 - {hipa_left} . 双膝不可过脚尖. 挺直背部. 收紧腹部核心.'
            else:
                score = score
                return '角度测算偏差过大.正面照片可以帮助我们对您的动作进行精确分析.'


def return_angle_bench_cn(img):
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
                if abs(int(bench_mins['bench_shoulder_to_knee_left'] - bench_mins['bench_shoulder_to_knee_right'])) <= 20:
                    if abs(int(bench_mins['bench_arm_to_hip_right'] - bench_mins['bench_arm_to_hip_left'])) <= 20:
                        if abs(int(bench_mins['bench_arm_to_shoulder_right'] - bench_mins['bench_arm_to_shoulder_left'])) <= 20:
                            score += 100
                            return f'分数 = {score} => 动作标准! 继续收紧腹部核心.'
                        else:
                            score += 50
                            as_right = bench_mins['bench_arm_to_shoulder_right']
                            as_left = bench_mins['bench_arm_to_shoulder_left']
                            return f'分数 = {score} => 双肘不平衡! 肘关节角度 : 右 - {as_right},左 - {as_left}. 肘关节与身侧尽量形成直角.'
                    else:
                        score += 30
                        ah_right = bench_mins['bench_arm_to_hip_right']
                        ah_left = bench_mins['bench_arm_to_hip_left']
                        return f'score = {score} => 双肩不平衡! 双肩角度 : 右 -{ah_right},左 - {ah_left}. 挺直背部. 收紧腹部核心. 避免将力量聚集在肩部和肘部!'
                else:
                    score += 30
                    sk_right = bench_mins['bench_shoulder_to_knee_right']
                    sk_left = bench_mins['bench_shoulder_to_knee_left']
                    return f'分数 = {score} => 身体不平衡!  臀部角度 : 右 - {sk_right},左 - {sk_left}. 保持肩臀膝三点一线. 收紧腹部核心. 腰部尽量向下贴近地面.'
            else:
                score = score
                return '角度测算偏差过大.正面照片可以帮助我们对您的动作进行精确分析.'


def return_angle_pushup_cn(img): #pushup angles need standardization
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
                if abs(int(pushup_mins_['pushup_shoulder_right'] - pushup_mins_['pushup_shoulder_left'])) <= 10:
                    if abs(int(pushup_mins_['pushup_arm_to_shoulder_right'] - pushup_mins_['pushup_arm_to_shoulder_left'])) <= 10:
                        if abs(int(pushup_mins_['pushup_head_to_ankle_right'] - pushup_mins_['pushup_head_to_ankle_left'])) <= 10:
                            score += 100
                            return f'分数 = {score} => 动作标准! 向下夹紧臀部肌肉. 挺直背部. 收紧腹部核心.'
                        else:
                            score += 50
                            ha_right = pushup_mins_['pushup_head_to_ankle_right']
                            ha_left = pushup_mins_['pushup_head_to_ankle_left']
                            return f'分数 = {score} => 双肩平衡! 但肩臀膝三点夹角过小! 臀部夹角 : 右 - {ha_right},左 - {ha_left}. 收紧腹部核心. 肩臀膝三点一线. 平行于地面. 左右侧面照可以让AI为您提供更精确的肩臀膝平衡分析.'
                    else:
                        score += 30
                        as_right = pushup_mins_['pushup_arm_to_shoulder_right']
                        as_left = pushup_mins_['pushup_arm_to_shoulder_left']
                        return f'分数 = {score} => 双肘不平衡! 肘关节角度 : 右 - {as_right},左 - {as_left}. 兼用双肘力量.避免手腕受力过大而受伤. 正面照片可以让AI为您提供更精确的肘关节平衡分析.'
                else:
                    score += 30
                    ha_right = pushup_mins_['pushup_shoulder_right']
                    ha_left = pushup_mins_['pushup_shoulder_left']
                    return f'分数 = {score} => 双肩不平衡! 双肩角度 : 右 -{ha_right},左 - {ha_left}. 兼用双肩力量. 挺直背部. 收紧腹部核心. 正面照片可以让AI为您提供更精确的双肩平衡分析.'
            else:
                score = score
                return '角度测算偏差过大.正面照片可以帮助我们对您的动作进行精确分析.'


def return_angle_bridge_cn(img):
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

            bridge_mins_ = standardize(bridge_mins)
            print(bridge_mins_)

            #algorithm for hip bridge
            right_sum = bridge_mins_['bridge_hip_to_ankle_right']+bridge_mins_['bridge_knee_to_toe_right']+bridge_mins_['bridge_shoulder_to_knee_right']
            left_sum = bridge_mins_['bridge_hip_to_ankle_left']+bridge_mins_['bridge_knee_to_toe_left']+bridge_mins_['bridge_shoulder_to_knee_left']

            if abs(int(right_sum - left_sum)) <= 30:
                if abs(int(bridge_mins_['bridge_shoulder_to_knee_right'] - bridge_mins_['bridge_shoulder_to_knee_left'])) <= 10:
                    if abs(int(bridge_mins_['bridge_hip_to_ankle_right'] - bridge_mins_['bridge_hip_to_ankle_left'])) <= 10:
                        if abs(int(bridge_mins_['bridge_knee_to_toe_right'] - bridge_mins_['bridge_knee_to_toe_left'])) <= 30:
                            if abs(int(bridge_mins_['bridge_hip_right'] - bridge_mins_['bridge_hip_left'])) <= 100:
                                score += 100
                                return f'分数 = {score} => 动作标准! 肩臀膝三点一线. 收紧腹部核心. 保持背部挺直.'
                            else:
                                score += 50
                                h_right = bridge_mins_['bridge_hip_right']
                                h_left = bridge_mins_['bridge_hip_left']
                                return f'分数 = {score} => 臀部不平衡! 臀部角度 :右 - {h_right},左 - {h_left}. 注意臀部发力. 避免伤及腰部.'
                        else:
                            score += 50
                            kt_right = bridge_mins_['bridge_knee_to_toe_right']
                            kt_left = bridge_mins_['bridge_knee_to_toe_left']
                            return f'分数 = {score} => 双腿不平行! 双膝与脚尖夹角 :右 - {kt_right},左 - {kt_left}. 保持膝盖与脚尖方向一致. 正面照片可以让AI为您提供更精确的平衡分析.'
                    else:
                        score += 30
                        ha_right = bridge_mins_['bridge_hip_to_ankle_right']
                        ha_left = bridge_mins_['bridge_hip_to_ankle_left']
                        return f'分数 = {score} => 双膝不平衡! 双膝角度 :右 - {ha_right},左 - {ha_left}. 保持两侧大腿互相平行. 小腿与地面呈直角.'
                else:
                    score += 30
                    sk_right = bridge_mins_['bridge_shoulder_to_knee_right']
                    sk_left = bridge_mins_['bridge_shoulder_to_knee_left']
                    return f'分数 = {score} => 身体不平衡! 臀部角度 :右 - {sk_right},左 - {sk_left}. 收紧腹部核心. 保持肩背臀膝形成一条直线.'

            else:
                score = score
                return '角度测算偏差过大.正面照片可以帮助我们对您的动作进行精确分析.'


if __name__ == "__main__":
    print(return_angle_bridge_cn(cv2.imread('raw_data/test_img/hip bridge/hipbridges402.jpeg')))
