import os
import subprocess
from tqdm import tqdm

# -------- CONFIG --------
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"

VIDEO_ROOT = "data/raw/videos"
AUDIO_ROOT = "data/raw/audio"

CLASSES = {
    "real": os.path.join(VIDEO_ROOT, "real"),
    "faceswap": os.path.join(VIDEO_ROOT, "fake", "faceswap"),
    "wav2lip": os.path.join(VIDEO_ROOT, "fake", "wav2lip"),
    "voiceclone": os.path.join(VIDEO_ROOT, "fake", "voiceclone"),
}

# ------------------------

def extract_audio_from_video(video_path, out_audio_path):
    subprocess.run(
        [
            FFMPEG,
            "-y",
            "-i", video_path,
            "-ac", "1",
            "-ar", "16000",
            out_audio_path
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def process_class(class_name, video_dir):
    if not os.path.exists(video_dir):
        return

    out_dir = os.path.join(AUDIO_ROOT, class_name)
    os.makedirs(out_dir, exist_ok=True)

    videos = [
        v for v in os.listdir(video_dir)
        if v.lower().endswith(".mp4")
    ]

    for video in tqdm(videos, desc=f"Extracting audio ({class_name})"):
        video_path = os.path.join(video_dir, video)
        audio_name = os.path.splitext(video)[0] + ".wav"
        audio_path = os.path.join(out_dir, audio_name)

        extract_audio_from_video(video_path, audio_path)


def main():
    for class_name, video_dir in CLASSES.items():
        process_class(class_name, video_dir)


if __name__ == "__main__":
    main()
