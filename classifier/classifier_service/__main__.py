# pylint: disable=too-many-locals, broad-except, no-member, unexpected-keyword-arg, bare-except, invalid-name, abstract-method, no-value-for-parameter, too-many-arguments, global-variable-undefined
"""
Classifier service. Requires trained model to run.
"""
import os
from io import BytesIO

import click
from flask import Flask, jsonify, make_response, request
from PIL import Image

from classifier_service.classification_result import ClassificationResult
from classifier_service.detect_alt import detect, get_model_and_device

app = Flask("classifier")

img_size = 640


@app.post("/classify")
def classify():
    """
    Classify image given in request body for defects.
    """
    try:
        confidence_threshold = float(request.args.get("confidence_threshold", 0.75))
    except ValueError:
        return make_response(
            f"Bad confidence_threshold is given: '{request.args['confidence_threshold']}' is not a number"
        )
    try:
        image = Image.open(BytesIO(request.get_data()))
        results: list[ClassificationResult] = detect(
            image, model, device, img_size, confidence_threshold=confidence_threshold
        )
    except Exception as exc:
        print(f"Exception occured: {exc!r}")
        return make_response(f"Error occured: {exc!r}", 400)

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
                " to get the results of its defects classification. ?conficence_treshold can also be specified."
            }
        )
    )


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
    "--weights",
    "-w",
    envvar="WEIGHTS_FILENAME",
    type=click.Path(exists=True, dir_okay=False),
    default="best.pt",
    show_default=True,
    show_envvar=True,
    help="Neural network weights after training process",
)
@click.option(
    "--image_size",
    "-h",
    envvar="IMAGE_SIZE",
    type=int,
    default=640,
    show_default=True,
    show_envvar=True,
    help="Max size to resize image before launching the neural network",
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
    weights: str,
    image_size: int,
    debug: bool,
):
    """
    CLI runner for classifier service.
    """
    global img_size  # pylint: disable=global-statement
    global model
    global device
    img_size = image_size

    model, device = get_model_and_device(weights, "cpu", img_size=img_size)

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
