from openai import OpenAI

from app.config import settings
from app.retriever import DocumentRetriever, SearchResult


class SmartCampusAgent:

    def __init__(self, retriever: DocumentRetriever):
        self.retriever = retriever

    def answer(
        self,
        question: str
    ) -> tuple[str, list[SearchResult]]:

        results = self.retriever.search(
            question=question,
            top_k=settings.top_k
        )

        if not results:
            return (
                "No encontré información suficiente en la documentación "
                "disponible para responder esta pregunta.",
                []
            )

        if not settings.openai_api_key:
            return self._local_answer(results), results

        return self._model_answer(question, results), results

    def _local_answer(
        self,
        results: list[SearchResult]
    ) -> str:
        best_result = results[0]

        return (
            "Información encontrada en la documentación:\n\n"
            f"{best_result.text}"
        )

    def _model_answer(
        self,
        question: str,
        results: list[SearchResult]
    ) -> str:

        context = "\n\n".join(
            (
                f"Fuente: {item.source}, "
                f"página o fila: {item.page}\n"
                f"{item.text}"
            )
            for item in results
        )

        client_options = {
            "api_key": settings.openai_api_key
        }

        if settings.openai_base_url:
            client_options["base_url"] = settings.openai_base_url

        client = OpenAI(**client_options)

        response = client.chat.completions.create(
            model=settings.openai_model,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un asistente académico. "
                        "Responde únicamente con información presente "
                        "en el contexto proporcionado. "
                        "Si el contexto no contiene la respuesta, indica "
                        "que no encontraste información suficiente. "
                        "No inventes datos."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Contexto:\n{context}\n\n"
                        f"Pregunta:\n{question}"
                    )
                }
            ]
        )

        content = response.choices[0].message.content

        if not content:
            return (
                "No fue posible generar una respuesta con la "
                "información disponible."
            )

        return content.strip()