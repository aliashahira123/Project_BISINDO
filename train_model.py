import os
import cv2
import mediapipe as mp
import numpy as np
import joblib

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# =========================
# DATASET PATH
# =========================
DATASET_PATH = "dataset_gambar"

# =========================
# MEDIAPIPE
# =========================
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5
)

# =========================
# DATASET
# =========================
X = []
y = []

print("Membaca dataset...")

for label in sorted(os.listdir(DATASET_PATH)):

    label_path = os.path.join(DATASET_PATH, label)

    if not os.path.isdir(label_path):
        continue

    print(f"Processing: {label}")

    for image_name in os.listdir(label_path):

        image_path = os.path.join(label_path, image_name)

        image = cv2.imread(image_path)

        if image is None:
            continue

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        if results.multi_hand_landmarks:

            left_hand = [0] * 63
            right_hand = [0] * 63

            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):

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

            final_data = left_hand + right_hand

            if len(final_data) == 126:

                X.append(final_data)
                y.append(label)

X = np.array(X)
y = np.array(y)

print(f"\nJumlah data: {len(X)}")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining model...")

model = ExtraTreesClassifier(
    n_estimators=500,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print(f"\nAkurasi: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

joblib.dump(model, "bisindo_model.pkl")

print("\nModel berhasil disimpan!")