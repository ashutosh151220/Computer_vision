import sys
import mediapipe as mp
import cv2
import numpy as np
from pose_detection_utils import calculate_angle,upper_body_cordinates,lower_body_cordinates
mp_drawing = mp.solutions.drawing_utils 
mp_pose = mp.solutions.pose 
counter=0
stage = "up"
if sys.argv[1]=="0":
    path=int(sys.argv[1])
else:
    path=sys.argv[1]
#cap = cv2.VideoCapture(r"D:\nptel deep learning\How To Squat Properly_ 3 Mistakes Harming Your Lower Back (FIX THESE!) (1).mp4")
cap = cv2.VideoCapture(path)
out = cv2.VideoWriter('pose_detection.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), 10,(1080,1080))
 
# Initiate holistic model
pose=mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)


while cap.isOpened():
    ret, frame = cap.read()
    
    # Recolor image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h,w,c=image.shape
    image.flags.writeable = False
    
    # Make detection
    results = pose.process(image)

    # Recolor back to BGR
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Extract landmarks
    try:
        landmarks = results.pose_landmarks.landmark
        
        # Get coordinates
        output=upper_body_cordinates(landmarks,mp_pose)
        #print(output.keys())
        
        # Calculate angle
        mode= sys.argv[2]
        if mode=="pushups":
            angle_right = calculate_angle(output["S_R"], output["E_R"], output["W_R"])
            angle_left=calculate_angle(output["S_L"], output["E_L"], output["W_L"])
            
            # Visualize angle
            cv2.putText(image, "right:"+str((angle_right)), 
                            tuple(np.multiply(output["E_R"], [w,h]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            cv2.putText(image, "left"+str(int(angle_left)), 
                            tuple(np.multiply(output["E_L"], [w,h]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            Hand="L"
            if Hand=="L":
                angle=int(angle_left)
            else:
                angle=int(angle_right)

            if angle < 90:
                    stage = "down"
            if angle > 160 and stage =='down':
                stage="up"
                counter +=1
                #print(counter)
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            # Stage data
            cv2.putText(image, 'STAGE', (65,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (60,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        if mode=="squat":
            output=lower_body_cordinates(landmarks,mp_pose)
            angle_right = calculate_angle(output["H_R"], output["K_R"], output["A_R"])
            angle_left=calculate_angle(output["H_L"], output["K_L"], output["A_L"])
            
            # Visualize angle
            cv2.putText(image, "right:"+str((angle_right)), 
                            tuple(np.multiply(output["K_R"], [w,h]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            cv2.putText(image, "left"+str(int(angle_left)), 
                            tuple(np.multiply(output["K_L"], [w,h]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            Hand="L"
            if Hand=="L":
                angle=int(angle_left)
            else:
                angle=int(angle_right)

            if angle < 90:
                    stage = "down"
            if angle > 150 and stage =='down':
                stage="up"
                counter +=1
                #print(counter)
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            # Stage data
            cv2.putText(image, 'STAGE', (65,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (60,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
                           
                    
    except :
        pass 
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                )               
   
    cv2.imshow('Mediapipe Feed', image);out.write(image) 
    

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
