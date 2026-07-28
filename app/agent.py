from openai import OpenAI
from app.config import settings
from app.retriever import DocumentRetriever, SearchResult


SYSTEM_PROMPT = """Eres el asistente de SmartCampus. Responde solo con la informacion incluida en el contexto. Si la respuesta no aparece, indica que no se encuentra en la documentacion disponible. Escribe en español claro y no inventes datos."""


class SmartCampusAgent:
    def __init__(self, retriever: DocumentRetriever):
        self.retriever = retriever

    def answer(self, question: str) -> tuple[str, list[SearchResult]]:
        results = self.retriever.search(question, settings.top_k)
        if not results:
            return "No encontre informacion relacionada en la documentacion disponible.", []

        if not settings.openai_api_key:
            summary = results[0].text
            return f"Informacion encontrada: {summary}", results

        kwargs = {"api_key": settings.openai_api_key}
        if settings.openai_base_url:
            kwargs["base_url"] = settings.openai_base_url
        client = OpenAI(**kwargs)

        context = "\n\n".join(
            f"Fuente: {item.source}, pagina o fila: {item.page}\n{item.text}"
            for item in results
        )
        response = client.chat.completions.create(
            model=settings.openai_model,
            temperature=0.1,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Contexto:\n{context}\n\nPregunta: {question}"},
            ],
        )
        return response.choices[0].message.content.strip(), results
