# Classifier service

This is a simple web-server which wait for the image on the /classify endpoint and return detected class boxes

It it not ment to be exposed to the outside world as the development server is used for YOLO inner C++ functions
  to work properly.

## Preparation

Before launch you need to download YOLOv7 repository and install its requirements. Current requirements must also be
  installed. The steps are listed in [prepare.sh file](prepare.sh). Virtual environment is used not to mess up system
  packages.

The trained YOLOv7 model will also be needed.

## Model training

**training** directory contains configuration files used for training. There are adapted tiny configuration from YOLOv7
  repository.

The following steps are not the one right way to do train the model, but an example of doing so.

0. Make sure thatyou have a GPU with enough Video Memory (tiny model consumes up to 10G at start and then works
  with ~6G). Install CUDA and properly GPU driver.

1. Get initial weights for tiny network you should download file and save it to the training/initial.pt (can be done
  with `wget -O training/initial.pt https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7-tiny.pt`)

2. Place images dataset to training/dataset and .txt files to training/labels

3. Activate virtual environment (`source venv/bin/activate` on Linux)

4. go to `training` directory and launch `python split.py` to split images to train, validate and test in given proportions

5. Begin neural network training with following command:
`python yolov7/train.py --weights training/initial.pt --cfg training/config.yaml --data training/dataset.yaml --hyp training/hyperparameters.yaml --epochs 8000 --img-size 640 640 --cache-images --adam --project ./training --name facades-tiny --save_period 500`

6. After training process copy **best.pt** file from training/facades-tiny/weights to /models

## Launching

After all of the requirements are installed and virtual environment is activated, and model weights file is obtained,
  server can be launched with `python -m classifier_service`. --help option could be used to get full commands list.