FROM python:3.8.6-buster

WORKDIR /aiworkout

COPY requirements.txt /aiworkout/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY api/fast.py /aiworkout/api/fast.py
COPY aiworkout /aiworkout/aiworkout
# COPY model.joblib /aiworkout/model.joblib
COPY credentials.json /aiworkout/credentials.json

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
