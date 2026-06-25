import cv2
import mediapipe as mp
import numpy as np
import joblib

# =========================
# LOAD MODEL
# =========================
model = joblib.load("bisindo_model.pkl")

# =========================
# MEDIAPIPE
# =========================
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# =========================
# CAMERA
# =========================
cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        left_hand = [0] * 63
        right_hand = [0] * 63

        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            handedness = results.multi_handedness[idx].classification[0].label

            temp = []

            wrist_x = hand_landmarks.landmark[0].x
            wrist_y = hand_landmarks.landmark[0].y
            wrist_z = hand_landmarks.landmark[0].z

            middle_x = hand_landmarks.landmark[9].x
            middle_y = hand_landmarks.landmark[9].y

            scale = np.sqrt(
                (middle_x - wrist_x) ** 2 +
                (middle_y - wrist_y) ** 2
            )

            if scale < 0.0001:
                scale = 1

            for lm in hand_landmarks.landmark:

                temp.append((lm.x - wrist_x) / scale)
                temp.append((lm.y - wrist_y) / scale)
                temp.append((lm.z - wrist_z) / scale)

            if handedness == "Left":
                left_hand = temp
            else:
                right_hand = temp

        data = left_hand + right_hand

        if len(data) == 126:

            landmarks = np.array(data).reshape(1, -1)

            prediction = model.predict(landmarks)[0]

            confidence = np.max(
                model.predict_proba(landmarks)
            )

            cv2.putText(
                frame,
                f"{prediction} ({confidence:.2f})",
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

    cv2.imshow("Deteksi BISINDO", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()