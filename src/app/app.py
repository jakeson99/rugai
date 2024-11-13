import streamlit as st
import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image

from ml_framework.model import NeuralNetworkWithDropout

# Load the model
model = NeuralNetworkWithDropout()
model.load_state_dict(torch.load('model/ckpt/NeuralNetworkWithDropout_20241110_214240_best.pt', map_location=torch.device('cpu')))
model.eval()

# Define preprocessing transform
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def predict(image):
    image = transform(image)
    image = image.unsqueeze(0) # Add batch dimension
    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)
    return predicted.item()

st.title("Image Classification App")
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    prediction = predict(image)
    st.write(f"Predicted class: {prediction}")