import cv2
import mediapipe as mp
import pyautogui
from eye_tracking import check_attention  # Import the check_attention function

import time

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils


last_action_time = 0
cooldown = 1  # sec

scroll_cooldown = 0.5 
last_scroll_time = 0
prev_y = None 
def detect_gesture(fingers):
    if fingers == [1, 1, 1, 1, 1]:
        return "Play"
    elif fingers == [0, 0, 0, 0, 0]:
        return "Pause"
    elif fingers == [0, 1, 1, 0, 0]:
        return "Volume Up"
    elif fingers == [0, 0, 0, 1, 1]:
        return "Volume Down"
    elif fingers == [0, 0, 0, 0, 1]:
        return "Next Video"
    elif fingers == [1, 1, 1, 1, 0]:
        return "Previous Video"
    else:
        return None

def fingers_up(hand_landmarks):
    fingers = []

    # 
    fingers.append(1 if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x else 0)

    tips_ids = [8, 12, 16, 20]
    for tip in tips_ids:
        fingers.append(1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y else 0)

    return fingers

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    check_attention(img)

    result = hands.process(img_rgb)

    gesture = None  

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            fingers = fingers_up(handLms)
            gesture = detect_gesture(fingers)

            print(f"Fingers: {fingers} -> Gesture: {gesture}")

            # Execute commands based on the detected gesture
            if gesture:
                current_time = time.time()
                if current_time - last_action_time > cooldown:
                    last_action_time = current_time

                    if gesture == "Play":
                        pyautogui.press("k")
                    elif gesture == "Pause":
                        pyautogui.press("k")
                    elif gesture == "Volume Up":
                        pyautogui.press("volumeup")
                    elif gesture == "Volume Down":
                        pyautogui.press("volumedown")
                    elif gesture == "Next Video":
                        pyautogui.hotkey("shift", "n")
                    elif gesture == "Previous Video":
                        pyautogui.hotkey("shift", "p")

            cy = handLms.landmark[9].y  

            if prev_y is not None:
                dy = prev_y - cy
                scroll_now = time.time()
                if scroll_now - last_scroll_time > scroll_cooldown:
                    if dy > 0.05:
                        pyautogui.scroll(300)
                        print("Scroll Up")
                        last_scroll_time = scroll_now
                    elif dy < -0.05:
                        pyautogui.scroll(-300)
                        print("Scroll Down")
                        last_scroll_time = scroll_now

            prev_y = cy

            cv2.putText(img, gesture or "", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    cv2.imshow("YouTube Gesture Controller", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
