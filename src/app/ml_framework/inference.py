from pathlib import Path

import torch
import yaml
from utils import load_preprocess_image

from ml_framework import ImprovedCNN


class ModelInference:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)
        self.class_dict = self.config["model_config"]["class_dict"]
        self.model_path = self.config["model_config"]["model_path"]
        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )
        self.model = self._load_model()
        self.model.to(self.device)

    def _load_model(self):
        model = ImprovedCNN(len(self.class_dict))
        state_dict = torch.load(
            self.model_path,
            map_location=self.device,
            weights_only=True,
        )
        model.load_state_dict(state_dict)
        model.eval()
        return model

    def _load_config(self, config_path):
        """Load and validate config file"""

        if isinstance(config_path, dict):
            config = config_path
        else:
            # Convert to Path object
            config_path = Path(config_path)

            # Check if file exists
            if not config_path.exists():
                raise FileNotFoundError(f"Config file not found: {config_path}")

            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
                print(config)

        # Validate required fields
        required_fields = ["class_dict"]
        for field in required_fields:
            if field not in config["model_config"]:
                raise ValueError(f"Missing required field: {field}")

        return config

    def inference(self, image_path):
        image = load_preprocess_image(image_path).to(self.device)
        self.model.eval()
        with torch.no_grad():
            output = self.model(image)
            probabilities = torch.nn.functional.softmax(output, dim=1)
            predicted_class = torch.argmax(probabilities).item()
            class_name = self.class_dict[predicted_class]
        return {
            "class": class_name,
            "probability": probabilities[0, predicted_class].item(),
        }
