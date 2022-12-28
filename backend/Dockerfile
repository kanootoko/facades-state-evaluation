FROM python:3.10-alpine

RUN apt update && apt install fonts-liberation

COPY requirements.txt /
RUN python3 -m pip install --no-cache-dir -r requirements.txt


COPY facades_api/ /facades_api/

ENTRYPOINT [ "python3", "-m", "facades_api" ]