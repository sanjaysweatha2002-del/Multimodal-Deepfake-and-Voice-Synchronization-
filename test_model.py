import torch
from model import MultimodalDeepfakeModel

model = MultimodalDeepfakeModel()

# Dummy inputs
face = torch.randn(1, 3, 224, 224)
mel = torch.randn(1, 1, 80, 100)

out = model(face, mel)

print("Output shape:", out.shape)
