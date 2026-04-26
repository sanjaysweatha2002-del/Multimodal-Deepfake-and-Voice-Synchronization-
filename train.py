import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from dataset import DeepfakeDataset
from model import MultimodalDeepfakeModel

# ------------------
# CONFIG
# ------------------
EPOCHS = 5
BATCH_SIZE = 2
LR = 1e-4
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# ------------------
# DATA
# ------------------
dataset = DeepfakeDataset(
    face_root="data/processed/faces",
    mel_root="data/processed/mels"
)

loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# ------------------
# MODEL
# ------------------
model = MultimodalDeepfakeModel().to(DEVICE)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LR)

# ------------------
# TRAIN LOOP
# ------------------
for epoch in range(EPOCHS):
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    for face, mel, label in loader:
        face = face.to(DEVICE)
        mel = mel.to(DEVICE)
        label = label.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(face, mel)

        loss = criterion(outputs, label)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        preds = torch.argmax(outputs, dim=1)
        correct += (preds == label).sum().item()
        total += label.size(0)

    acc = correct / total * 100
    print(f"Epoch [{epoch+1}/{EPOCHS}]  Loss: {total_loss:.4f}  Accuracy: {acc:.2f}%")

# ------------------
# SAVE MODEL
# ------------------
torch.save(model.state_dict(), "multimodal_deepfake_model.pth")
print("Model saved!")
