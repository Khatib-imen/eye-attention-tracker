import cv2
import mediapipe as mp
import time
import threading
import winsound

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]
CENTER_NOSE = 1

last_focus_time = time.time()
ALERT_DELAY = 2
is_alert_playing = False
alarm_thread = None

def is_looking_center(landmarks, img_w, img_h):
    try:
        nose_x = landmarks[CENTER_NOSE].x * img_w
        left_x = landmarks[LEFT_EYE[0]].x * img_w
        right_x = landmarks[RIGHT_EYE[0]].x * img_w
        return left_x < nose_x < right_x
    except:
        return True

def check_attention(img):
    global last_focus_time, is_alert_playing, alarm_thread

    h, w, _ = img.shape
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            left_eye_x = int(face_landmarks.landmark[LEFT_EYE[0]].x * w)
            left_eye_y = int(face_landmarks.landmark[LEFT_EYE[0]].y * h)
            right_eye_x = int(face_landmarks.landmark[RIGHT_EYE[0]].x * w)
            right_eye_y = int(face_landmarks.landmark[RIGHT_EYE[0]].y * h)

            cv2.circle(img, (left_eye_x, left_eye_y), 5, (0, 255, 0), -1)  
            cv2.circle(img, (right_eye_x, right_eye_y), 5, (0, 255, 0), -1) 

            if not is_looking_center(face_landmarks.landmark, w, h):
                if time.time() - last_focus_time > ALERT_DELAY and not is_alert_playing:
                    print("Attention lost, playing alert.")
                    is_alert_playing = True
                    alarm_thread = threading.Thread(target=play_alarm)
                    alarm_thread.start()
            else:
                last_focus_time = time.time()
                if is_alert_playing:
                    print("User refocused, stopping alarm.")
                    stop_alarm()
                    is_alert_playing = False

def play_alarm():
    print("Playing alarm sound!")
    winsound.PlaySound("alarm.wav", winsound.SND_FILENAME)

def stop_alarm():
    
    print("Alarm stopped!")

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        if not success:
            break

        check_attention(img)  

        cv2.imshow("Eye Tracking", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
