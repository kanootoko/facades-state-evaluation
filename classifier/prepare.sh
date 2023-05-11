#!/bin/sh
git clone https://github.com/WongKinYiu/yolov7 yolov7

python -m venv venv

source venv/bin/activate

python -m pip install -r yolov7/requirements.txt

python -m pip install -r requirements.txt