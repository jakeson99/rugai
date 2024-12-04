# rugai  🧞‍♂️
Rugai is a project which uses a convolutional neural network to classify the origin of antique rug images.
The model is trained locally and accessed via the application deployed on Streamlit Cloud.

## Getting Started
Rugai can be accessed via Streamlit Cloud:
[rugai](https://therugai.streamlit.app/)

If you'd like to run any of the code locally, first clone the repository. Package dependencies are handled via [Poetry](https://python-poetry.org/docs/). Once Poetry is installed on your system you can install dependencies and activate the environment using:
```
cd rugai
poetry install
poetry shell
```

To run the rugai streamlit application locally use the following command:
```
streamlit run src/app/app.py
```

The model training was done via a jupyter notebook which can be run using:

```
jupyter notebook notebooks/model_training_updated.ipynb
```

To run the web scraper and download training images first update `.env` with the appropriate variables and run the following command:
```
cd src 
poetry run python scraper_runner.py
```


