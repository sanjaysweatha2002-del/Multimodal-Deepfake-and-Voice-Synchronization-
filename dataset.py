import os
import torch
from torch.utils.data import Dataset
from PIL import Image
from torchvision import transforms

CLASS_MAP = {
    "real": 0,
    "faceswap": 1,
    "wav2lip": 2,
    "voiceclone": 3
}

face_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


class DeepfakeDataset(Dataset):
    def __init__(self, face_root, mel_root):
        self.samples = []

        for cls, label in CLASS_MAP.items():
            face_cls_dir = os.path.join(face_root, cls)
            mel_cls_dir = os.path.join(mel_root, cls)

            if not os.path.exists(face_cls_dir) or not os.path.exists(mel_cls_dir):
                continue

            for video_name in os.listdir(face_cls_dir):
                face_dir = os.path.join(face_cls_dir, video_name)
                mel_path = os.path.join(mel_cls_dir, video_name + ".npy")

                if not os.path.isdir(face_dir):
                    continue

                if not os.path.exists(mel_path):
                    continue

                self.samples.append((face_dir, mel_path, label))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        face_dir, mel_path, label = self.samples[idx]

        # Load first face image
        face_files = sorted(os.listdir(face_dir))
        face_img = Image.open(os.path.join(face_dir, face_files[0])).convert("RGB")
        face = face_transform(face_img)

        mel = torch.tensor(
            __import__("numpy").load(mel_path)
        ).unsqueeze(0).float()

        return face, mel, label
