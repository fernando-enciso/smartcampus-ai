import re
import unicodedata
from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SPANISH_STOP_WORDS = {
    "a", "al", "algo", "como", "con", "cual", "cuando", "de", "del",
    "donde", "el", "ella", "en", "es", "esta", "este", "hay", "la",
    "las", "lo", "los", "me", "mi", "para", "por", "que", "se", "si",
    "sin", "sobre", "su", "sus", "un", "una", "uno", "y"
}


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text.lower())

    return "".join(
        character
        for character in normalized
        if unicodedata.category(character) != "Mn"
    )


def meaningful_tokens(text: str) -> set[str]:
    normalized = normalize_text(text)
    words = re.findall(r"\b[a-z0-9]+\b", normalized)

    return {
        word
        for word in words
        if word not in SPANISH_STOP_WORDS and len(word) > 2
    }


def split_text(
    text: str,
    max_words: int = 180,
    overlap: int = 35
) -> list[str]:
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
                self.chunks.append({
                    **document,
                    "text": chunk,
                    "tokens": meaningful_tokens(chunk)
                })

        if not self.chunks:
            raise ValueError(
                "No se encontraron documentos para indexar."
            )

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            ngram_range=(1, 2),
            stop_words=list(SPANISH_STOP_WORDS)
        )

        self.matrix = self.vectorizer.fit_transform(
            [item["text"] for item in self.chunks]
        )

    def search(
        self,
        question: str,
        top_k: int = 5,
        min_score: float = 0.08
    ) -> list[SearchResult]:
        question = question.strip()

        if not question:
            return []

        question_tokens = meaningful_tokens(question)

        if not question_tokens:
            return []

        query = self.vectorizer.transform([question])
        scores = cosine_similarity(query, self.matrix).flatten()
        indexes = scores.argsort()[::-1]

        results = []

        for index in indexes:
            score = float(scores[index])
            chunk = self.chunks[index]

            common_tokens = question_tokens.intersection(
                chunk["tokens"]
            )

            if not common_tokens:
                continue

            if score < min_score:
                continue

            results.append(
                SearchResult(
                    text=chunk["text"],
                    source=chunk["source"],
                    page=chunk["page"],
                    score=score
                )
            )

            if len(results) >= top_k:
                break

        return results