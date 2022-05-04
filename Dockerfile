FROM python:3.8.6-buster

WORKDIR /aiworkoutassistant_prediction_api

COPY requirements.txt /aiworkoutassistant_prediction_api/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY api/fast.py /aiworkoutassistant_prediction_api/api/fast.py
COPY aiworkout /aiworkoutassistant_prediction_api/aiworkout
COPY credentials.json /aiworkoutassistant_prediction_api/credentials.json

CMD uvicorn api.fast:app --host 0.0.0.0 --port 3000
