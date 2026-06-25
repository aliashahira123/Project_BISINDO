import cv2
import mediapipe as mp
import os
import csv

# =========================
# MEDIAPIPE HANDS
# =========================
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5
)

# =========================
# PATH DATASET
# =========================
dataset_path = "dataset_gambar"
csv_file = "dataset_tangan.csv"

# =========================
# BUKA FILE CSV
# =========================
with open(csv_file, mode='w', newline='') as f:

    writer = csv.writer(f)

    # Header CSV
    header = ["label"]

    for i in range(126):
        header.append(f"x{i}")

    writer.writerow(header)

    # =========================
    # LOOP LABEL
    # =========================
    for label in os.listdir(dataset_path):

        label_path = os.path.join(dataset_path, label)

        # Skip jika bukan folder
        if not os.path.isdir(label_path):
            continue

        print(f"\nProcessing Label: {label}")

        # =========================
        # LOOP GAMBAR
        # =========================
        for img_name in os.listdir(label_path):

            img_path = os.path.join(label_path, img_name)

            img = cv2.imread(img_path)

            if img is None:
                continue

            # Convert RGB
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Deteksi tangan
            result = hands.process(rgb)

            # =========================
            # JIKA TANGAN TERDETEKSI
            # =========================
            if result.multi_hand_landmarks:

                data = []

                # Ambil landmark semua tangan
                for hand_landmarks in result.multi_hand_landmarks:

                    # Wrist normalisasi
                    wrist_x = hand_landmarks.landmark[0].x
                    wrist_y = hand_landmarks.landmark[0].y
                    wrist_z = hand_landmarks.landmark[0].z

                    # 21 landmark
                    for lm in hand_landmarks.landmark:

                        data.append(lm.x - wrist_x)
                        data.append(lm.y - wrist_y)
                        data.append(lm.z - wrist_z)

                # Jika hanya 1 tangan
                if len(result.multi_hand_landmarks) == 1:
                    data.extend([0] * 63)

                # Pastikan jumlah fitur 126
                if len(data) == 126:

                    row = [label] + data

                    writer.writerow(row)

                    print(f"Berhasil: {img_name}")

print("\nEkstraksi landmark selesai!")