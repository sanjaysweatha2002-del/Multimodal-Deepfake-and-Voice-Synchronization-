import torch
import torch.nn as nn
import timm

# -------------------------
# AUDIO ENCODER (CNN)
# -------------------------
class AudioEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1))
        )

    def forward(self, x):
        x = self.conv(x)
        return x.view(x.size(0), -1)


# -------------------------
# MULTIMODAL MODEL
# -------------------------
class MultimodalDeepfakeModel(nn.Module):
    def __init__(self):
        super().__init__()

        # Vision Transformer (Face)
        self.vision_encoder = timm.create_model(
            "vit_base_patch16_224",
            pretrained=True,
            num_classes=0
        )

        # Audio Encoder
        self.audio_encoder = AudioEncoder()

        # Fusion + Classifier
        self.classifier = nn.Sequential(
            nn.Linear(768 + 128, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 4)  # real vs fake (fake:faceswap, wav2lip, voiceclone)
        )

    def forward(self, face, mel):
        face_feat = self.vision_encoder(face)
        audio_feat = self.audio_encoder(mel)

        fused = torch.cat([face_feat, audio_feat], dim=1)
        return self.classifier(fused)
