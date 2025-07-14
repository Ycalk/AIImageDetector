import torch
from PIL import Image
from torchvision import transforms


class Model:
    def __init__(self, model_path: str) -> None:
        self.model = torch.jit.load(model_path)
        self.model.eval()
        self.transforms = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Resize((256, 256)),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
            ]
        )

    def __call__(self, image: Image.Image) -> float:
        tensor: torch.Tensor = self.transforms(image)  # type: ignore
        with torch.no_grad():
            output = self.model(tensor.unsqueeze(0))

        return torch.sigmoid(output).item()
