import cv2
import os

# =========================
# INPUT LABEL
# =========================
label = input("Masukkan label gesture: ")

# =========================
# FOLDER DATASET
# =========================
DATASET_DIR = "dataset_gambar"

# Folder per label
save_dir = os.path.join(DATASET_DIR, label)

# Buat folder jika belum ada
os.makedirs(save_dir, exist_ok=True)

# =========================
# BUKA KAMERA
# =========================
cap = cv2.VideoCapture(0)

# Hitung jumlah file yang sudah ada
count = len(os.listdir(save_dir))

print("===================================")
print(f"Label : {label}")
print("Tekan S untuk simpan gambar")
print("Tekan Q untuk keluar")
print("===================================")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Flip kamera
    frame = cv2.flip(frame, 1)

    # Tampilkan jumlah data
    cv2.putText(
        frame,
        f"Jumlah Data: {count}",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Tampilkan kamera
    cv2.imshow("Collect Dataset BISINDO", frame)

    key = cv2.waitKey(1)

    # =========================
    # SIMPAN GAMBAR
    # =========================
    if key == ord('s'):

        # Nama file gambar
        img_name = f"{count}.jpg"

        # Path lengkap
        img_path = os.path.join(save_dir, img_name)

        # Simpan gambar
        cv2.imwrite(img_path, frame)

        count += 1

        print(f"Gambar disimpan: {img_path}")

    # =========================
    # KELUAR
    # =========================
    if key == ord('q'):
        break

# =========================
# RELEASE
# =========================
cap.release()
cv2.destroyAllWindows()