from torch import nn
import torch
import numpy as np
import cv2
from PIL import Image
from torchvision import transforms


class GradCam:
    """Генерация Grad-CAM для заданной модели и слоя."""

    def __init__(self, model: nn.Module, target_layer: nn.Module, image: Image.Image):
        """Инициализация GradCam.

        Args:
            model (nn.Module): Модель для генерации Grad-CAM.
            target_layer (nn.Module): Слой, для которого будет вычисляться Grad-CAM.
            image (Image.Image): Изображение, для которого будет вычисляться Grad-CAM.
        """
        self.model = model
        self.target_layer = target_layer
        self.image = image

    def __call__(self) -> tuple[np.ndarray, float]:
        """Генерация Grad-CAM для заданного изображения.

        Returns:
            tuple[np.ndarray, float]: Кортеж, содержащий наложение Grad-CAM на изображение и оценку модели для этого изображения.
        """
        device = next(self.model.parameters()).device
        self.model.eval()

        activations: list[torch.Tensor] = []
        gradients: list[torch.Tensor] = []

        self.target_layer.register_forward_hook(
            lambda _, __, output: activations.append(output.detach())
        )
        self.target_layer.register_backward_hook(
            lambda _, __, grad_out: gradients.append(grad_out[0].detach())
        )

        transform = transforms.Compose(
            [
                transforms.Resize((256, 256)),
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
            ]
        )

        input_tensor: torch.Tensor = (
            transform(self.image).unsqueeze(0).to(device)  # type: ignore
        )

        output = self.model(input_tensor)
        score = output[0]
        self.model.zero_grad()
        score.backward()

        grads = gradients[0][0]
        acts = activations[0][0]
        weights = grads.mean(dim=(1, 2))

        cam = torch.zeros(acts.shape[1:], dtype=torch.float32).to(device)
        for i, w in enumerate(weights):
            cam += w * acts[i]
        cam = torch.relu(cam).to(device)

        cam -= cam.min()
        cam /= cam.max()
        result_cam = np.uint8(255 * cv2.resize(cam.cpu().numpy(), (256, 256)))

        heatmap = cv2.applyColorMap(result_cam, cv2.COLORMAP_JET)  # type: ignore
        overlay = cv2.addWeighted(
            np.array(self.image.resize((256, 256))), 0.5, heatmap, 0.5, 0
        )

        return overlay, score.item()
