# rugai

Rugai is a project which uses deep learning to predict the origin of rug images.

## Getting Started
Rugai can be accessed via [Streamlit Cloud](https://therugai.streamlit.app/).


To run the web scraper and download training images first update `.env` with the appropriate variables and run the following command:
```
cd src 
poetry run python scraper_runner.py
```

To run the rugai streamlit application locally use the following command:
```
streamlit run src/app/app.py
```
