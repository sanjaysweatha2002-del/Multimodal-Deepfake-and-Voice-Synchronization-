from dataset import DeepfakeDataset

dataset = DeepfakeDataset(
    face_root="data/processed/faces",
    mel_root="data/processed/mels"
)

print("Total samples:", len(dataset))

face, mel, label = dataset[0]
print("Face shape:", face.shape)
print("Mel shape:", mel.shape)
print("Label:", label)
