import re
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def split_text(text: str, max_words: int = 180, overlap: int = 35) -> list[str]:
    words = re.findall(r"\S+", text)
    if not words:
        return []
    chunks = []
    step = max(1, max_words - overlap)
    for start in range(0, len(words), step):
        part = words[start:start + max_words]
        if part:
            chunks.append(" ".join(part))
        if start + max_words >= len(words):
            break
    return chunks


@dataclass
class SearchResult:
    text: str
    source: str
    page: int
    score: float


class DocumentRetriever:
    def __init__(self, documents: list[dict]):
        self.chunks = []
        for document in documents:
            for chunk in split_text(document["text"]):
                self.chunks.append({**document, "text": chunk})
        if not self.chunks:
            raise ValueError("No se encontraron contenidos para indexar.")
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), strip_accents="unicode", lowercase=True)
        self.matrix = self.vectorizer.fit_transform([item["text"] for item in self.chunks])

    def search(self, question: str, top_k: int = 5) -> list[SearchResult]:
        query = self.vectorizer.transform([question])
        scores = cosine_similarity(query, self.matrix).flatten()
        indexes = scores.argsort()[::-1][:top_k]
        return [
            SearchResult(
                text=self.chunks[index]["text"],
                source=self.chunks[index]["source"],
                page=self.chunks[index]["page"],
                score=float(scores[index]),
            )
            for index in indexes
            if scores[index] > 0
        ]
