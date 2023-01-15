# pylint: disable=dangerous-default-value
"""
Defects drawing functions are defined here.
"""
from PIL import Image, ImageDraw, ImageFont

from facades_api.dto import ClassificationResult

default_color = (60, 60, 60, 120)


def draw_defects(
    photo: Image.Image,
    defects: list[ClassificationResult],
    colors: dict[str, tuple[int, int, int, int]] = {
        "bricks": (180, 10, 10, 60),
        "wall_damage": (250, 128, 40, 60),
        "crack": (190, 180, 0, 60),
        "construction": (110, 210, 140, 60),
    },
) -> Image.Image:
    """
    Mark defects with colored rectangles and return image.
    """
    photo_with_defects = photo.convert("RGB")
    if len(defects) == 0:
        return photo_with_defects
    draw = ImageDraw.Draw(photo_with_defects, "RGBA")
    try:
        font = ImageFont.truetype("arial", photo.width // 150)
    except OSError:
        font = ImageFont.truetype("LiberationSans-Regular", photo.width // 150)

    for defect in defects:
        draw.rectangle(
            (
                defect.box[0] * photo.width,
                defect.box[1] * photo.height,
                (defect.box[0] + defect.box[2]) * photo.width,
                (defect.box[1] + defect.box[3]) * photo.height,
            ),
            fill=colors.get(defect.class_name),
        )
        box = font.getbbox(str(defect.class_name))
        _text_w, text_h = box[2] - box[0], box[3] - box[1]
        draw.text(
            (
                (defect.box[0]) * photo.width,
                (defect.box[1]) * photo.height - text_h,
            ),
            f"{defect.class_name} ({defect.confidence*100:.1f})",
            fill=(0, 0, 0, 180),
            font=font,
        )
    return photo_with_defects
