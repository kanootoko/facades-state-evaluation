FROM python:3.10-slim

ARG WEIGHTS_FILENAME=*.weights
ARG CFG_FILENAME=*.cfg
ARG CLASSES_FILENAME=classes.txt

RUN apt update && apt install -y libgl-dev libglib2.0-0

RUN mkdir /app

COPY requirements.txt /app/

RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt

COPY classifier_service.py /app/

COPY $WEIGHTS_FILENAME /app/
COPY $CFG_FILENAME /app/
COPY $CLASSES_FILENAME /app/

WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["classifier_service.py"]