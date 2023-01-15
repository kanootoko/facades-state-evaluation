# pylint: disable=too-many-locals, broad-except, no-member, unexpected-keyword-arg, bare-except, invalid-name, abstract-method, no-value-for-parameter, too-many-arguments, global-variable-undefined
"""
Classifier service. Requires trained model to run.
"""
import os
import platform
import uuid
from dataclasses import dataclass
from io import BytesIO

import click
import cv2
from flask import Flask, jsonify, make_response, request
from numpy import argmax


@dataclass(frozen=True)
class Result:
    """
    Classification result class.
    """

    box: tuple[float, float, float, float]
    confidence: float
    class_name: str


app = Flask("classifier")


@app.post("/classify")
def classify():
    """
    Classify image given in request body for defects.
    """
    img_data = BytesIO(request.get_data())

    path = str(uuid.uuid4())
    try:
        with open(path, "wb") as file:
            file.write(img_data.getvalue())
        img = cv2.imread(path)
    except Exception as ex:
        return make_response(f"Error occured: {ex}", code=400)
    finally:
        try:
            os.remove(path)
        except:
            pass

    blob = cv2.dnn.blobFromImage(img, 1 / 255, (image_size[0], image_size[1]), (0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(net.getUnconnectedOutLayersNames())

    results: list[Result] = []

    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = int(argmax(scores))
            confidence = round(float(scores[class_id]), 3)
            if confidence > 0.2:
                center_x = round(float(detection[0]), 6)
                center_y = round(float(detection[1]), 6)
                w = round(float(detection[2]), 6)
                h = round(float(detection[3]), 6)

                x = center_x - w / 2
                y = center_y - h / 2

                results.append(Result((x, y, w, h), confidence, classes[class_id]))

    return make_response(jsonify({"defects": results}))


@app.get("/")
def basic_help():
    """
    Return small help message on opening root page.
    """
    return make_response(
        jsonify(
            {
                "help": "Send image in body parameter to /classify endpoint"
                " to get the results of its defects classification"
            }
        )
    )


if platform.uname().system.lower() == "linux":
    print("Detected Linux, Preparing gunicorn")
    import gunicorn.app.base

    class StandaloneApplication(gunicorn.app.base.BaseApplication):
        """
        WSGI application wrapper.
        """

        def __init__(self, application, options: dict | None = None):
            self.options = options if options is not None else {}
            self.application = application
            super().__init__()

        def load_config(self):
            config = {
                key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None
            }
            for key, cfg_value in config.items():
                self.cfg.set(key.lower(), cfg_value)

        def load(self):
            return self.application


@click.command("classifier")
@click.option(
    "--port",
    "-p",
    envvar="PORT",
    type=int,
    default=8081,
    show_default=True,
    show_envvar=True,
    help="Service port number",
)
@click.option(
    "--host",
    envvar="HOST",
    default="0.0.0.0",
    show_default=True,
    show_envvar=True,
    help="Service HOST address (0.0.0.0 to accept requests from everywhere)",
)
@click.option(
    "--weights_filename",
    "-w",
    envvar="WEIGHTS_FILENAME",
    default="training_last.weights",
    show_default=True,
    show_envvar=True,
    help="Neural network weights after training process",
)
@click.option(
    "--cfg_filename",
    "-c",
    envvar="CFG_FILENAME",
    default="training.cfg",
    show_default=True,
    show_envvar=True,
    help="Neural network training configuration after training process",
)
@click.option(
    "--classes_filename",
    "-C",
    envvar="CLASSES_FILENAME",
    default="classes.txt",
    show_default=True,
    show_envvar=True,
    help="Neural network training classes list",
)
@click.option(
    "--image_width",
    "-w",
    envvar="IMAGE_WIDTH",
    type=int,
    default=416,
    show_default=True,
    show_envvar=True,
    help="Width to resize image before launching the neural network",
)
@click.option(
    "--image_height",
    "-h",
    envvar="IMAGE_HEIGHT",
    type=int,
    default=416,
    show_default=True,
    show_envvar=True,
    help="Height to resize image before launching the neural network",
)
@click.option(
    "--debug",
    envvar="DEBUG",
    is_flag=True,
    help="Enable debug mode (auto-reload on change, traceback returned to user, etc.)",
)
def main(
    port: int,
    host: str,
    weights_filename: str,
    cfg_filename: str,
    classes_filename: str,
    image_width: int,
    image_height: int,
    debug: bool,
):
    """
    CLI runner for classifier service.
    """
    global net
    global classes
    global image_size
    net = cv2.dnn.readNet(weights_filename, cfg_filename)
    with open(classes_filename, "r", encoding="utf-8") as file:
        classes = file.read().splitlines()
    image_size = (image_width, image_height)
    if platform.uname().system.lower() == "linux":
        options = {
            "bind": f"{host}:{port}",
            "workers": 1,
            "timeout": 120,
            "debug": debug,
        }
        StandaloneApplication(app, options).run()
    else:
        app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    envfile = os.environ.get("ENVFILE", ".env")
    if os.path.isfile(envfile):
        with open(envfile, "rt", encoding="utf-8") as f:
            for name, value in (
                tuple((line[len("export ") :] if line.startswith("export ") else line).strip().split("=", 1))
                for line in f.readlines()
                if not line.startswith("#") and "=" in line
            ):
                if name not in os.environ:
                    if " #" in value:
                        value = value[: value.index(" #")]
                    os.environ[name] = value.strip()
    main()
