import re
from pathlib import Path
from datetime import datetime


def sanitize_filename(
    text: str
):

    text = re.sub(
        r'[<>:"/\\|?*]',
        "_",
        text
    )

    return text[:50]


def timestamp():

    return datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )


def ensure_directory(
    folder: str
):

    Path(folder).mkdir(
        parents=True,
        exist_ok=True
    )