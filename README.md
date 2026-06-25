\# 🤟 BISINDO — Real-Time Indonesian Sign Language Detection System



A real-time web-based application for detecting Indonesian Sign Language (BISINDO) using webcam input, MediaPipe, Flask, and Machine Learning.



\---



\# 📌 Features



\* Real-time hand gesture detection using webcam

\* Hand landmark extraction using MediaPipe

\* BISINDO sign classification using Machine Learning

\* Web-based interface with Flask backend

\* Real-time prediction display

\* Dataset collection and model training support



\---



\# 📁 Project Structure



```text

Project\_BISINDO/

│

├── Backend/

│   ├── app.py

│   ├── requirements.txt

│   │

│   ├── templates/

│   │   └── index.html

│   │

│   └── static/

│       ├── css/

│       │   └── style.css

│       │

│       └── js/

│           └── script.js

│

├── collect\_dataset.py

├── extract\_landmark.py

├── realtime\_detection.py

├── train\_model.py

├── dataset\_tangan.csv

├── README.md

└── .gitignore

```



\---



\# ⚙️ Installation



\## 1️⃣ Clone Repository



```bash

git clone https://github.com/aliashahira123/Project\_BISINDO.git

```



\---



\## 2️⃣ Move into Project Folder



```bash

cd Project\_BISINDO

```



\---



\## 3️⃣ Install Dependencies



```bash

pip install -r Backend/requirements.txt

```



\---



\# ▶️ Run the Application



\## Run Flask Server



```bash

python Backend/app.py

```



If successful:



```text

==================================================

🤟 BISINDO Detection System - Server Active

==================================================

URL: http://localhost:5000

Model: ✅ Loaded

==================================================

```



\---



\# 🌐 Open in Browser



Open your browser and visit:



```text

http://localhost:5000

```



\---



\# 🎥 How to Use



1\. Click \*\*"Mulai Kamera"\*\*

2\. Allow browser camera access

3\. Point your hand toward the webcam

4\. Perform BISINDO gestures

5\. Prediction results will appear automatically



\---



\# 🎯 Supported Detection



| Category | Example                                  |

| -------- | ---------------------------------------- |

| Letters  | A - Z                                    |

| Numbers  | 0 - 10                                   |

| Words    | ibu, rahasia, tolong, mulai, adik, bagus |



\---



\# 🛠️ Tech Stack



\* Frontend: HTML5, CSS3, JavaScript

\* Backend: Flask + Flask-CORS

\* Computer Vision: OpenCV + MediaPipe Hands

\* Machine Learning: Scikit-learn

\* Communication: REST API + Fetch API



\---



\# 📂 Dataset



Dataset is available on Kaggle:



\[PUT YOUR KAGGLE DATASET LINK HERE]



\---



\# 🧠 Machine Learning Model



The trained `.pkl` model is available on Kaggle:



\[PUT YOUR MODEL LINK HERE]



\---



\# ⚠️ Troubleshooting



| Problem               | Solution                                  |

| --------------------- | ----------------------------------------- |

| Model not found       | Make sure the `.pkl` model exists locally |

| Camera access denied  | Allow camera permission in browser        |

| Hand not detected     | Improve lighting conditions               |

| Prediction inaccurate | Retrain using more dataset images         |



\---



\# 🚀 Future Improvements



\* Add more BISINDO vocabulary

\* Improve prediction accuracy

\* Deploy to cloud/web hosting

\* Mobile application support

\* Sentence generation from gestures



\---



\# 👩‍💻 Author



\*\*Alia Shahira\*\*



Computer Vision \& Machine Learning Project



