from torchvision.models import resnet18, ResNet18_Weights
from torch import nn
import torch


class ResNetModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
        self.model.fc = nn.Linear(512, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)


if __name__ == "__main__":
    model = ResNetModel()
    print(model)
    example_input = torch.randn(1, 3, 224, 224)
    output = model(example_input)
    print(output.shape)
