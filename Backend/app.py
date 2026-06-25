from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe as mp
import numpy as np
import joblib
import os
from collections import deque

app = Flask(__name__)

# =========================
# LOAD MODEL (OUTSIDE BACKEND)
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "bisindo_model.pkl")

model = joblib.load(MODEL_PATH)
print("MODEL LOADED")

# =========================
# MEDIAPIPE
# =========================
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    model_complexity=0,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

# =========================
# STATE SYSTEM
# =========================
sentence = []
word_buffer = ""
last_token = ""
stable_buffer = deque(maxlen=7)

FIXED_WORDS = ["IBU", "TOLONG", "RAHASIA", "BAGUS", "MULAI", "ADIK"]

# =========================
# SMART TOKEN PROCESSOR
# =========================
def process_token(token):
    global word_buffer, last_token, sentence

    stable_buffer.append(token)

    if len(stable_buffer) < 7:
        return

    final = max(set(stable_buffer), key=stable_buffer.count)

    # ❌ anti spam
    if final == last_token:
        return
    last_token = final

    # =========================
    # KATA FIXED
    # =========================
    if final in FIXED_WORDS:
        if word_buffer:
            sentence.append(word_buffer)
            word_buffer = ""
        sentence.append(final)
        return

    # =========================
    # HURUF / ANGKA
    # =========================
    if len(final) == 1 or final.isdigit():
        if final.isalnum():
            word_buffer += final
        return


# =========================
# RESET WORD BUFFER
# =========================
def flush_word():
    global word_buffer
    if word_buffer:
        sentence.append(word_buffer)
        word_buffer = ""


# =========================
# ROUTES
# =========================
@app.route('/')
def index():
    return render_template("index.html")


def generate():
    global sentence

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = hands.process(rgb)

        detected = ""

        if result.multi_hand_landmarks:

            left = [0]*63
            right = [0]*63

            for i, hand in enumerate(result.multi_hand_landmarks):

                handed = result.multi_handedness[i].classification[0].label

                wrist = hand.landmark[0]
                mid = hand.landmark[9]

                scale = np.sqrt((mid.x-wrist.x)**2 + (mid.y-wrist.y)**2)
                if scale == 0:
                    scale = 1

                temp = []
                for lm in hand.landmark:
                    temp += [(lm.x-wrist.x)/scale,
                             (lm.y-wrist.y)/scale,
                             (lm.z-wrist.z)/scale]

                if handed == "Left":
                    left = temp
                else:
                    right = temp

            data = np.array(left + right).reshape(1, -1)

            if data.shape[1] == 126:
                pred = model.predict(data)[0]
                process_token(pred)
                detected = pred

        # ================= UI =================
        cv2.rectangle(frame, (0,0), (1280,120), (245,235,220), -1)

        cv2.putText(frame, f"DETEKSI: {detected}",
                    (20,50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (50,50,50), 2)

        cv2.putText(frame, f"OUTPUT: {' '.join(sentence)}",
                    (20,90), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (80,80,80), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/sentence')
def get_sentence():
    return jsonify({"sentence": " ".join(sentence)})


@app.route('/reset')
def reset():
    global sentence, word_buffer, last_token, stable_buffer

    sentence = []
    word_buffer = ""
    last_token = ""
    stable_buffer.clear()

    return jsonify({"status": "ok"})


@app.route('/space')
def space():
    flush_word()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print("SERVER RUNNING")
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)