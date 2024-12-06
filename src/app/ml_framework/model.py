import torch.nn.functional as F
from torch import nn
from torchvision import models


def load_resnet50(num_classes: int = 7):
    """Load the model architecture for the ResNet50 model."""
    model = models.resnet50(pretrained=False)

    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, num_classes)

    return model
