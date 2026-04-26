import torch
import cv2
import numpy as np
import librosa
import tempfile
import subprocess
import streamlit as st
from torchvision import transforms
from PIL import Image
from model import MultimodalDeepfakeModel

# ---------------- CONFIG ----------------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"
MAX_MEL_LEN = 400
NUM_FRAMES = 5
CONF_THRESHOLD = 60
CLASS_NAMES = {0: "Real", 1: "FaceSwap", 2: "Wav2Lip", 3: "VoiceClone"}

face_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

@st.cache_resource(show_spinner=False)
def load_model():
    model = MultimodalDeepfakeModel().to(DEVICE)
    model.load_state_dict(torch.load("multimodal_deepfake_model.pth", map_location=DEVICE))
    model.eval()
    return model

def extract_faces(video_path):
    cap = cv2.VideoCapture(video_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total <= 0:
        cap.release()
        return None
    idxs = np.linspace(0, total - 1, NUM_FRAMES, dtype=int)
    tensors = []
    for idx in idxs:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue
        tensors.append(face_transform(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))))
    cap.release()
    return torch.stack(tensors) if tensors else None

def extract_audio(video_path):
    audio_path = video_path.replace(".mp4", ".wav")
    subprocess.run(
        [FFMPEG, "-y", "-i", video_path, "-ac", "1", "-ar", "16000", audio_path],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return audio_path

def extract_mel(audio_path):
    y, sr = librosa.load(audio_path, sr=16000)
    mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=80, n_fft=400, hop_length=160)
    mel = librosa.power_to_db(mel)
    if mel.shape[1] < MAX_MEL_LEN:
        mel = np.pad(mel, ((0, 0), (0, MAX_MEL_LEN - mel.shape[1])))
    else:
        mel = mel[:, :MAX_MEL_LEN]
    return torch.tensor(mel).unsqueeze(0).unsqueeze(0).float()

def run_inference(video_path, model):
    faces = extract_faces(video_path)
    audio_path = extract_audio(video_path)
    mel = extract_mel(audio_path)

    if faces is None:
        return None

    faces = faces.to(DEVICE)
    mel = mel.to(DEVICE)

    probs_list = []
    with torch.no_grad():
        for i in range(faces.size(0)):
            out = model(faces[i].unsqueeze(0), mel)
            probs_list.append(torch.softmax(out, dim=1))

    probs = torch.cat(probs_list, dim=0)
    probs = probs[torch.argmax(probs.max(dim=1).values)]
    pred_class = torch.argmax(probs).item()
    confidence = probs[pred_class].item() * 100

    if confidence < CONF_THRESHOLD:
        label = "Possibly Fake / Uncertain"
        badge_color = "#fbbf24"
        icon = "?"
    elif pred_class == 0:
        label = "Real"
        badge_color = "#22c55e"
        icon = "✓"
    else:
        label = CLASS_NAMES[pred_class]
        badge_color = "#ef4444"
        icon = "✗"

    return {
        "label": label,
        "confidence": confidence,
        "badge_color": badge_color,
        "icon": icon,
        "probs": probs.cpu().numpy()
    }