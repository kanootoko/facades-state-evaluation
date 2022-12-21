FROM python:3.10

RUN apt update && apt install fonts-liberation

COPY requirements.txt /
RUN python3 -m pip install -r requirements.txt


COPY facades_api/ /facades_api/

ENTRYPOINT [ "python3", "-m", "facades_api" ]