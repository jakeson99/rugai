import streamlit as st
import yaml
from ml_framework import ModelInference
from PIL import Image

st.set_page_config(page_title="RugAI", page_icon=":genie:", layout="wide")

# Load config
with open("src/app/config/config.yaml") as f:
    config = yaml.safe_load(f)


def main():
    st.title(":genie: RugAI")
    st.subheader("Determine the origin of your vintage rug!")
    st.write("Upload an image to begin!")

    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    col1, col2 = st.columns([1, 1])

    if uploaded_file is not None:
        # Display image
        image = Image.open(uploaded_file)
        col1.image(image, caption="Uploaded Image", use_container_width=True)

    if uploaded_file is not None and col1.button("Classify Image"):
        with st.spinner("Analyzing image..."):
            model = ModelInference(config)
            prediction = model.inference(uploaded_file)

        st.success(f"Predicted Class: {prediction['class']}")
        st.write(f"Confidence: {prediction['probability']:.2%}")
        st.progress(prediction["probability"])


if __name__ == "__main__":
    main()
