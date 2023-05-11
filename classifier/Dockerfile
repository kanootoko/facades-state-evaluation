FROM python:3.10-slim

ARG WEIGHTS_FILENAME=*.pt

RUN apt update && apt install -y libgl-dev libglib2.0-0

RUN apt install -y git \
    && mkdir -p /app/model \
    && git clone https://github.com/WongKinYiu/yolov7 /app/yolov7 \
    && apt purge -y --autoremove git \
    && python -m pip install --no-cache-dir -r /app/yolov7/requirements.txt

COPY requirements.txt /app/

RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt

COPY classifier_service /app/

COPY $WEIGHTS_FILENAME /app/model/

WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["-m", "classifier_service"]