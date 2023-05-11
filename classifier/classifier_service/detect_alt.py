"""
Detect classes on a given photo.

Should be put inside YOLOv7 sources directory.
"""
import sys
from pathlib import Path

import click
import numpy as np
import torch
from PIL import Image

sys.path.append(str(Path(__name__).resolve().parent / "yolov7/"))

from models.experimental import attempt_load # pylint: disable=wrong-import-position
from utils.datasets import letterbox
from utils.general import check_img_size, non_max_suppression, scale_coords, xyxy2xywh
from utils.torch_utils import TracedModel, select_device


try:
    from classifier_service.classification_result import ClassificationResult
except ImportError:
    from classification_result import ClassificationResult


def detect(  # pylint: disable=too-many-arguments,too-many-locals
    image: Image.Image,
    model,
    device,
    img_size: int,
    confidence_threshold: float = 0.25,
    iou_threshold: float = 0.45,
):
    """
    Detect given image classes and return them as list.
    """
    names = model.module.names if hasattr(model, "module") else model.names

    # Run inference
    if device.type != "cpu":
        model(
            torch.zeros(1, 3, img_size, img_size)  # pylint: disable=no-member
            .to(device)
            .type_as(next(model.parameters()))
        )

    stride = int(model.stride.max())  # model stride
    img_size = check_img_size(img_size, s=stride)  # check img_size

    img0 = np.asarray(image)
    img1 = letterbox(img0, img_size, stride=stride)[0]

    # Convert
    img1 = img1[:, :, :].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img1 = np.ascontiguousarray(img1)

    img = torch.from_numpy(img1).to(device)  # pylint: disable=no-member

    img = img.half() if device.type != "cpu" else img.float()  # uint8 to fp16/32

    img /= 255.0  # 0 - 255 to 0.0 - 1.0

    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    # Inference
    with torch.no_grad():  # Calculating gradients would cause a GPU memory leak
        pred = model(img, augment=False)[0]  # <<--- here TensorShape

    # Apply NMS
    pred = non_max_suppression(pred, confidence_threshold, iou_threshold)

    # Process detections
    detected: list[ClassificationResult] = []
    for det in pred:  # detections per image
        g_n = torch.tensor(img0.shape)[[1, 0, 1, 0]]  # pylint: disable=no-member
        if len(det):
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()

            for *xyxy, conf, cls in det:
                xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / g_n).view(-1).tolist()  # pylint: disable=no-member
                detected.append(
                    ClassificationResult.from_yolo(
                        int(cls), *xywh, (names[int(cls)] if int(cls) < len(names) else None), float(conf)
                    )
                )

    return detected


def get_model_and_device(weights: str, device: str, trace: bool = False, img_size: int = 640) -> tuple:
    """
    Get model and device instances.

    If trace is set to true, returns traced model.

    img_size is only used with traced model.
    """
    actual_device = select_device(device)
    half = actual_device.type != "cpu"  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=actual_device)  # load FP32 model

    if trace:
        model = TracedModel(model, actual_device, img_size)

    if half:
        model.half()  # to FP16

    return model, actual_device


@click.command("detect")
@click.option(
    "--weights",
    "-w",
    envvar="WEIGHTS",
    type=click.Path(exists=True, dir_okay=False),
    default="models/best.pt",
    help="model.pt path",
    show_default=True,
    show_envvar=True,
)
@click.option(
    "--output",
    "-o",
    envvar="OUTPUT_TXT",
    type=click.Path(dir_okay=False),
    default=None,
    help="Output detection txt path",
    show_default=True,
    show_envvar=True,
)
@click.option(
    "--img_size",
    "-s",
    envvar="IMG_SIZE",
    type=int,
    default=640,
    help="Size of the image to run through the neural network",
    show_default=True,
    show_envvar=True,
)
@click.option(
    "--confidence_threshold",
    "-c",
    envvar="CONFIDENCE_THRESHOLD",
    type=click.FloatRange(0.0, 1.0),
    default=0.25,
    help="Confidence threshold value",
    show_default=True,
    show_envvar=True,
)
@click.option(
    "--iou_threshold",
    "-i",
    envvar="IOU_THRESHOLD",
    type=click.FloatRange(0.0, 1.0),
    default=0.45,
    help="IOU threshold value",
    show_default=True,
    show_envvar=True,
)
@click.option(
    "--device",
    "-d",
    envvar="DEVICE",
    default="cpu",
    help="Device to run calculations on, e.g. '0', '1', 'cpu'",
    show_default=True,
    show_envvar=True,
)
@click.option("--trace", "-t", envvar="TRACE", is_flag=True, help="If model should be traced")
@click.argument("source", type=click.Path(exists=True, dir_okay=False))
def main(  # pylint: disable=too-many-arguments
    weights: str,
    output: None | str,
    img_size: int,
    confidence_threshold: float,
    iou_threshold: float,
    device: str,
    trace: bool,
    source: str,
):
    """
    Run model and get detected boxes as YOLO txts.
    """
    model, actual_device = get_model_and_device(weights, device, trace)

    image = Image.open(source)

    with torch.no_grad():
        classes = detect(image, model, actual_device, img_size, confidence_threshold, iou_threshold)

    with torch.no_grad():
        classes = detect(image, model, actual_device, img_size, confidence_threshold, iou_threshold)

    if output is None:
        print(f"Detected {len(classes)} boxes")
        print("\n".join(map(str, classes)))
    else:
        Path(output).write_text(
            "\n".join(
                (
                    " ".join((map(lambda x: f"{x:.6f}" if isinstance(x, float) else str(x), cls.to_yolo())))
                    for cls in classes
                )
            ),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
