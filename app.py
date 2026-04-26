import streamlit as st

# MUST be the first Streamlit command
st.set_page_config(
    page_title="Multimodal Deepfake Source Attribution",
    layout="centered"
)

import torch
import cv2
import numpy as np
import librosa
import tempfile
import subprocess
from torchvision import transforms
from PIL import Image
from model import MultimodalDeepfakeModel

# ---------------- CONFIG ----------------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"
MAX_MEL_LEN = 400
NUM_FRAMES = 5
CONF_THRESHOLD = 60  # percent

CLASS_NAMES = {
    0: "Real",
    1: "FaceSwap",
    2: "Wav2Lip",
    3: "VoiceClone"
}

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    model = MultimodalDeepfakeModel().to(DEVICE)
    model.load_state_dict(
        torch.load("multimodal_deepfake_model.pth", map_location=DEVICE)
    )
    model.eval()
    return model

model = load_model()

# ---------------- TRANSFORMS ----------------
face_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ---------------- HELPER FUNCTIONS ----------------
def extract_faces(video_path, num_frames=NUM_FRAMES):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames <= 0:
        cap.release()
        return None

    frame_indices = np.linspace(
        0, total_frames - 1, num_frames, dtype=int
    )

    face_tensors = []

    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        face_tensors.append(face_transform(img))

    cap.release()

    if len(face_tensors) == 0:
        return None

    # Shape: [num_frames, 3, 224, 224]
    return torch.stack(face_tensors)


def extract_audio(video_path):
    audio_path = video_path.replace(".mp4", ".wav")
    subprocess.run(
        [FFMPEG, "-y", "-i", video_path, "-ac", "1", "-ar", "16000", audio_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return audio_path


def extract_mel(audio_path):
    y, sr = librosa.load(audio_path, sr=16000)
    mel = librosa.feature.melspectrogram(
        y=y, sr=sr, n_mels=80, n_fft=400, hop_length=160
    )
    mel = librosa.power_to_db(mel)

    if mel.shape[1] < MAX_MEL_LEN:
        mel = np.pad(mel, ((0, 0), (0, MAX_MEL_LEN - mel.shape[1])))
    else:
        mel = mel[:, :MAX_MEL_LEN]

    return torch.tensor(mel).unsqueeze(0).unsqueeze(0).float()

# ---------------- STREAMLIT UI ----------------
st.title("🎭 Multimodal Deepfake Detection & Source Attribution")
st.write(
    "Upload a video to detect whether it is **Real** or **Fake**, "
    "and if fake, identify the **source of manipulation** "
    "(FaceSwap / Wav2Lip / VoiceClone)."
)

uploaded_video = st.file_uploader("Upload a video", type=["mp4"])

if uploaded_video:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded_video.read())
        video_path = tmp.name

    st.video(video_path)

    if st.button("Analyze Video"):
        with st.spinner("Analyzing video..."):
            faces = extract_faces(video_path)
            audio_path = extract_audio(video_path)
            mel = extract_mel(audio_path)

            if faces is None:
                st.error("❌ Failed to extract frames from video.")
            else:
                faces = faces.to(DEVICE)
                mel = mel.to(DEVICE)
                # 🔧 TEMPORARY DEBUG: ignore audio completely
                # mel = torch.zeros_like(mel).to(DEVICE)
                probs_list = []

                with torch.no_grad():
                    for i in range(faces.size(0)):
                        face_i = faces[i].unsqueeze(0)
                        output = model(face_i, mel)
                        probs = torch.softmax(output, dim=1)
                        probs_list.append(probs)

                # Average probabilities across frames
                #probs = torch.mean(torch.cat(probs_list, dim=0), dim=0)
                
                # Take the most confident frame instead of averaging
                probs = torch.cat(probs_list, dim=0)
                probs = probs[torch.argmax(probs.max(dim=1).values)]

                pred_class = torch.argmax(probs).item()
                confidence = probs[pred_class].item() * 100

                if confidence < CONF_THRESHOLD:
                    label = "Possibly Fake / Uncertain"
                else:
                    label = CLASS_NAMES[pred_class]

                st.success("✅ Analysis Complete")
                st.subheader(f"🧠 Prediction: **{label}**")
                st.write(f"📊 Confidence: **{confidence:.2f}%**")

                st.bar_chart(probs.cpu().numpy())