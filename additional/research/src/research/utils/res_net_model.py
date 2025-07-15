from torchvision.models import resnet18, ResNet18_Weights
from torch import nn
import torch


class ResNetModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.features = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
        self.features.fc = nn.Identity() # type: ignore
        self.fc = nn.Sequential(
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 1),
        )

    def freeze_features(self) -> None:
        for param in self.features.parameters():
            param.requires_grad = False

    def unfreeze_features(self) -> None:
        for param in self.features.parameters():
            param.requires_grad = True

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        features = self.features(x)
        return self.fc(features)


if __name__ == "__main__":
    model = ResNetModel()
    print(model)
    example_input = torch.randn(1, 3, 224, 224)
    output = model(example_input)
    print(output.shape)
