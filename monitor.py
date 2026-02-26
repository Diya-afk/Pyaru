import cv2
import mediapipe as mp
import time
import winsound

# Initialize MediaPipe face detection
mp_face = mp.solutions.face_detection
face = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.6)

# Start webcam
cap = cv2.VideoCapture(0)

last_alert = 0   # prevents continuous sound

def alert():
    global last_alert
    if time.time() - last_alert > 3:   # 3 sec cooldown
        print("ALERT TRIGGERED")
        winsound.PlaySound("alert.wav",
                           winsound.SND_FILENAME | winsound.SND_ASYNC)
        last_alert = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR to RGB for mediapipe
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face.process(rgb)

    # Detection logic
    if result.detections:
        status = "Focused ho arey waahhhh"
        color = (0, 255, 0)
    else:
        status = "padh le kutte vrna bahot pitega!!"
        color = (0, 0, 255)
        alert()

    # Display status on screen
    cv2.putText(frame, status, (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                color, 2)

    cv2.imshow("Focus Monitor", frame)

    # Press ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()