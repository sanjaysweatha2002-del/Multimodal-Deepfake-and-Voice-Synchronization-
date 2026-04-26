import os
import cv2
from tqdm import tqdm

VIDEO_ROOT = "data/raw/videos"
OUT_ROOT = "data/processed/faces"

CLASSES = {
    "real": os.path.join(VIDEO_ROOT, "real"),
    "faceswap": os.path.join(VIDEO_ROOT, "fake", "faceswap"),
    "wav2lip": os.path.join(VIDEO_ROOT, "fake", "wav2lip"),
    "voiceclone": os.path.join(VIDEO_ROOT, "fake", "voiceclone"),
}

def extract_faces_from_video(video_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    frame_id = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # save every 10th frame (enough for training)
        if frame_id % 10 == 0:
            frame_path = os.path.join(out_dir, f"{frame_id}.jpg")
            cv2.imwrite(frame_path, frame)

        frame_id += 1

    cap.release()


def process_class(class_name, video_dir):
    if not os.path.exists(video_dir):
        return

    out_class_dir = os.path.join(OUT_ROOT, class_name)
    os.makedirs(out_class_dir, exist_ok=True)

    videos = [
        v for v in os.listdir(video_dir)
        if v.lower().endswith(".mp4")
    ]

    for video in tqdm(videos, desc=f"Processing {class_name.upper()}"):
        video_path = os.path.join(video_dir, video)
        video_name = os.path.splitext(video)[0]
        out_video_dir = os.path.join(out_class_dir, video_name)

        extract_faces_from_video(video_path, out_video_dir)


def main():
    for class_name, video_dir in CLASSES.items():
        process_class(class_name, video_dir)


if __name__ == "__main__":
    main()
