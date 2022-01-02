import cv2
import mediapipe as mp
import time
import controller as cnt
import pyttsx3

engine= pyttsx3.init() # Voice assistant module

print("1 for Ambulance")
print("2 for Police")
print("3 for Fire Department")  # Emergency Menu
print("4 for Gendarme")
print("5 for AFAD")

engine.say("Please select an emergency service or press q if you want to exit.") # Assistant asked for making a choice
engine.runAndWait()




time.sleep(2.0)

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

tipIds = [4, 8, 12, 16, 20]

video = cv2.VideoCapture(0)

with mp_hand.Hands(min_detection_confidence=0.5,
                   min_tracking_confidence=0.5) as hands:
    while True:
        ret, image = video.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmList = []
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands = results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)
        fingers = []                      # Codes for detecting fingers
        if len(lmList) != 0:
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total = fingers.count(1)
            cnt.led(total)

            if total == 1:   #If camera detects 1 finger

                engine.say("You called an ambulance . Your location has been taken and ambulance is on the way")
                engine.runAndWait()

            elif total == 2:  #If camera detects 2 fingers

                engine.say("You called the police . Your location has been taken and the police is on the way")
                engine.runAndWait()

            elif total == 3:  #If camera detects 3 fingers

                engine.say("You called the fire department . Your location has been taken and firemen are on the way")
                engine.runAndWait()


            elif total == 4:  #If camera detects 4 fingers
                engine.say("You called the gendarme . Your location has been taken and gendarme is on the way")
                engine.runAndWait()


            elif total == 5: #If camera detects 5 fingers
                engine.say("You called AFAD . Your location has been taken and rescue team is on the way.")
                engine.runAndWait()




        cv2.imshow("Frame", image)
        k = cv2.waitKey(1)
        if k == ord('q'):  # key for quit from system
            break
video.release()
cv2.destroyAllWindows()
