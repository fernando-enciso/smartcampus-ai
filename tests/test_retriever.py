from app.retriever import DocumentRetriever


def test_search_returns_related_content():
    documents = [
        {"text": "La nota minima de aprobacion es 4,0.", "source": "reglamento.pdf", "page": 1},
        {"text": "El enlace de contraseña dura 30 minutos.", "source": "guia.pdf", "page": 2},
    ]
    retriever = DocumentRetriever(documents)
    results = retriever.search("¿Cual es la nota minima?", 1)
    assert results
    assert "4,0" in results[0].text
