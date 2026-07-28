import streamlit as st
from dotenv import load_dotenv

from app.agent import SmartCampusAgent
from app.config import settings
from app.loaders import load_documents
from app.retriever import DocumentRetriever

load_dotenv()

st.set_page_config(
    page_title="SmartCampus AI",
    page_icon="🎓",
    layout="centered"
)


@st.cache_resource
def build_agent():
    documents = load_documents(settings.documents_dir)
    retriever = DocumentRetriever(documents)

    return SmartCampusAgent(retriever), len(documents)


st.title("🎓 SmartCampus AI")

st.caption(
    "Consulta reglamentos, guías, preguntas frecuentes y el catálogo de cursos."
)

try:
    agent, document_count = build_agent()

except Exception as error:
    st.error(f"No fue posible cargar la documentación: {error}")
    st.stop()

st.success(
    f"Base documental cargada correctamente ({document_count} registros)."
)

examples = [
    "¿Cuál es la nota mínima para aprobar?",
    "¿Cómo recupero mi contraseña?",
    "¿Qué cursos duran diez semanas?",
    "¿Cuál es el curso más económico?",
    "¿Cómo solicito un certificado?"
]

question = st.text_input(
    "Escribe tu pregunta",
    placeholder=examples[0]
)

selected = st.selectbox(
    "O selecciona una consulta de ejemplo",
    [""] + examples
)

if selected and not question:
    question = selected

if st.button(
    "Consultar",
    type="primary",
    use_container_width=True
):

    if not question.strip():
        st.warning("Escribe una pregunta antes de continuar.")

    else:

        with st.spinner("Buscando en la documentación..."):

            try:
                answer, sources = agent.answer(question.strip())

            except Exception as error:
                st.error(f"No fue posible generar la respuesta: {error}")

            else:

                st.subheader("Respuesta")

                st.write(answer)

                if sources:

                    with st.expander("Fuentes consultadas"):

                        for item in sources:

                            st.markdown(
                                f"**{item.source} — página o fila {item.page}**"
                            )

                            st.caption(
                                f"Coincidencia: {item.score:.1%}"
                            )

                            st.write(
                                item.text[:500]
                                + (
                                    "..."
                                    if len(item.text) > 500
                                    else ""
                                )
                            )

st.divider()

if settings.openai_api_key:
    st.caption(
        f"Modelo configurado: {settings.openai_model}"
    )
else:
    st.caption(
        "Modo local: búsqueda documental mediante similitud TF-IDF."
    )