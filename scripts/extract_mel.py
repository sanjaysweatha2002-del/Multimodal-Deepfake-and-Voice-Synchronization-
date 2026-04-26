import os
import librosa
import numpy as np
from tqdm import tqdm

RAW_AUDIO_DIR = "data/raw/audio"
OUT_MEL_DIR = "data/processed/mels"

SAMPLE_RATE = 16000
N_MELS = 80
N_FFT = 400
HOP_LENGTH = 160
MAX_MEL_LEN = 400


def process_class(class_name):
    in_dir = os.path.join(RAW_AUDIO_DIR, class_name)
    out_dir = os.path.join(OUT_MEL_DIR, class_name)
    os.makedirs(out_dir, exist_ok=True)

    for audio_file in tqdm(os.listdir(in_dir), desc=f"Processing {class_name}"):
        if not audio_file.endswith(".wav"):
            continue

        audio_path = os.path.join(in_dir, audio_file)
        mel_path = os.path.join(out_dir, audio_file.replace(".wav", ".npy"))

        y, sr = librosa.load(audio_path, sr=SAMPLE_RATE)

        mel = librosa.feature.melspectrogram(
            y=y,
            sr=sr,
            n_mels=N_MELS,
            n_fft=N_FFT,
            hop_length=HOP_LENGTH
        )

        mel = librosa.power_to_db(mel)

        # Pad / truncate
        if mel.shape[1] < MAX_MEL_LEN:
            mel = np.pad(mel, ((0, 0), (0, MAX_MEL_LEN - mel.shape[1])))
        else:
            mel = mel[:, :MAX_MEL_LEN]

        np.save(mel_path, mel)


def main():
    classes = ["real", "faceswap", "wav2lip", "voiceclone"]

    for cls in classes:
        cls_dir = os.path.join(RAW_AUDIO_DIR, cls)
        if os.path.exists(cls_dir):
            process_class(cls)


if __name__ == "__main__":
    main()
