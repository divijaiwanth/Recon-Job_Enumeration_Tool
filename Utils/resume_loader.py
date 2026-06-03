from pathlib import Path

from pypdf import PdfReader


def load_resume(
    file_path: str
):

    path = Path(file_path)

    if not path.exists():

        raise FileNotFoundError(
            file_path
        )

    suffix = (
        path.suffix.lower()
    )

    # --------------------
    # TXT
    # --------------------

    if suffix == ".txt":

        return path.read_text(
            encoding="utf-8"
        )

    # --------------------
    # MD
    # --------------------

    if suffix == ".md":

        return path.read_text(
            encoding="utf-8"
        )

    # --------------------
    # PDF
    # --------------------

    if suffix == ".pdf":

        reader = PdfReader(
            str(path)
        )

        text = ""

        for page in reader.pages:

            text += (
                page.extract_text()
                + "\n"
            )

        return text

    raise ValueError(
        f"Unsupported file type: {suffix}"
    )