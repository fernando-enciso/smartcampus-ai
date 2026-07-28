from pathlib import Path
import csv
from pypdf import PdfReader


def load_pdf(path: Path) -> list[dict]:
    reader = PdfReader(str(path))
    items = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            items.append({"text": text, "source": path.name, "page": page_number})
    return items


def load_csv(path: Path) -> list[dict]:
    items = []
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row_number, row in enumerate(reader, start=2):
            text = "; ".join(f"{key}: {value}" for key, value in row.items())
            items.append({"text": text, "source": path.name, "page": row_number})
    return items


def load_documents(directory: str) -> list[dict]:
    base = Path(directory)
    documents = []
    for path in sorted(base.glob("*")):
        if path.suffix.lower() == ".pdf":
            documents.extend(load_pdf(path))
        elif path.suffix.lower() == ".csv":
            documents.extend(load_csv(path))
    return documents
