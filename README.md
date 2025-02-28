# rugai  🧞‍♂️
Rugai is a project which uses a convolutional neural network to classify the origin of vintage rug images.
The model is trained locally and the UI is created using Streamlit and deployed on Streamlit Cloud.

## Getting started

Rugai can be accessed via Streamlit Cloud:
[rugai](https://therugai.streamlit.app/)


An example of the UI can be seen below:
![rugai UI](https://github.com/user-attachments/assets/b3cfe886-e001-4c22-968e-cf438bfc0aa9)

To begin drag and drop an image of your rug or click 'Browse files' and select the image you wish to classify. A preview of the image will then appear. To run the prediction click 'Classify'. The model will then return the predicted origin of the uploaded image along with a confidence score.

## How it works

The model is a convolutional neaural net with a fully connected final layer as the classifier. It was trained on 7 classes representing the different rug origins. Training was done locally using [mps backend](https://pytorch.org/docs/stable/notes/mps.html) on the GPU of a M1 macbook and experiment tracking was done using [Weights and Biases](https://wandb.ai/site). The UI was created using the [Streamlit framework](https://streamlit.io/) and deployed on [Streamlit Cloud](https://streamlit.io/cloud).

## Run from source

If you'd like to run any of the code locally, first clone the repository. Package dependencies are handled via [Poetry](https://python-poetry.org/docs/). Once Poetry is installed on your system you can install dependencies and activate the environment using:
```
cd rugai
poetry install
poetry shell
```

To run the rugai streamlit application locally use the following command:
```
streamlit run rugai/app/app.py
```

The model training was done via a jupyter notebook which can be run using:

```
jupyter notebook notebooks/model_training_updated.ipynb
```

To run the web scraper and download training images first update `.env` with the appropriate variables and run the following command:
```
cd rugai 
poetry run python scraper_runner.py
```


