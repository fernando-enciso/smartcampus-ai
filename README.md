# SmartCampus AI

Agente de consulta documental para una plataforma educativa ficticia. Permite realizar preguntas sobre reglamentos, uso de la plataforma, privacidad, reembolsos, tareas docentes y oferta de cursos.

## Objetivo

Centralizar la informacion academica y administrativa para que estudiantes y docentes puedan encontrar respuestas sin revisar manualmente cada documento.

## Funcionalidades

- Lectura de documentos PDF.
- Lectura de datos desde CSV.
- Division e indexacion del contenido.
- Busqueda por similitud mediante TF-IDF.
- Respuestas generadas con un modelo compatible con la API de OpenAI.
- Funcionamiento local sin API, mostrando el fragmento mas relevante.
- Visualizacion de las fuentes utilizadas.
- Interfaz web con Streamlit.
- Ejecucion mediante Docker.

## Arquitectura

```text
Usuario
  |
  v
Interfaz Streamlit
  |
  v
SmartCampusAgent
  |
  +--> Recuperador TF-IDF
  |       |
  |       +--> PDF y CSV
  |
  +--> Modelo de lenguaje
```

La aplicacion carga los documentos al iniciar, divide el texto en fragmentos e indexa cada fragmento. Cuando se recibe una pregunta, recupera los contenidos mas relacionados y los entrega al modelo como contexto. La respuesta se limita a la informacion disponible.

## Tecnologias

- Python 3.11
- Streamlit
- pypdf
- scikit-learn
- OpenAI SDK
- Docker
- Oracle Cloud Infrastructure Compute

## Documentos incluidos

- Reglamento del estudiante.
- Guia de uso de la plataforma.
- Preguntas frecuentes.
- Politica de privacidad.
- Politica de cancelaciones y reembolsos.
- Manual para docentes.
- Catalogo de cursos en CSV.

## Ejecucion local

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/smartcampus-ai.git
cd smartcampus-ai
```

### 2. Crear un entorno virtual

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Linux o macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables

Windows:

```powershell
copy .env.example .env
```

Linux o macOS:

```bash
cp .env.example .env
```

Completar `OPENAI_API_KEY` en `.env`. Sin una clave, el proyecto funciona en modo local y muestra el fragmento documental mas relevante.

### 5. Iniciar la aplicacion

```bash
streamlit run app/main.py
```

Abrir `http://localhost:8501`.

## Ejecucion con Docker

Crear el archivo `.env` y luego ejecutar:

```bash
docker compose up --build
```

Tambien puede ejecutarse sin Compose:

```bash
docker build -t smartcampus-ai .
docker run --env-file .env -p 8501:8501 smartcampus-ai
```

## Preguntas de ejemplo

- ¿Cual es la nota minima para aprobar un curso?
- ¿Que debo hacer para recuperar mi contraseña?
- ¿Cuanto demora un reembolso aprobado?
- ¿Que cursos duran diez semanas?
- ¿Cual es el curso mas economico?
- ¿Durante cuanto tiempo se conservan los registros academicos?
- ¿En cuanto tiempo debe calificarse una tarea?

## Respuestas esperadas

**Pregunta:** ¿Cual es la nota minima para aprobar un curso?

**Respuesta:** La nota minima de aprobacion es 4,0. En los cursos con clases en vivo tambien debe cumplirse la asistencia minima indicada en el reglamento.

**Pregunta:** ¿Cuanto demora un reembolso aprobado?

**Respuesta:** La devolucion se procesa dentro de diez dias habiles desde su aprobacion. La acreditacion del banco o emisor puede tardar hasta diez dias habiles adicionales.

## Pruebas

```bash
pip install pytest
pytest
```

## Despliegue en OCI Compute

1. Crear una instancia de OCI Compute con Ubuntu.
2. Configurar una regla de ingreso TCP para el puerto 8501.
3. Conectarse por SSH.
4. Instalar Git y Docker.
5. Clonar el repositorio.
6. Crear el archivo `.env`.
7. Ejecutar `docker compose up -d --build`.
8. Acceder mediante `http://IP_PUBLICA:8501`.

## Evidencia del despliegue

Agregar en `screenshots/` una captura de la aplicacion funcionando en OCI y completar los siguientes datos antes de la entrega:

- URL publica: `PENDIENTE`
- Fecha del despliegue: `PENDIENTE`
- Captura: `screenshots/deploy-oci.png`

## Estructura

```text
smartcampus-ai/
├── app/
│   ├── agent.py
│   ├── config.py
│   ├── loaders.py
│   ├── main.py
│   └── retriever.py
├── documents/
├── screenshots/
├── tests/
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Alcance

SmartCampus es una plataforma ficticia creada exclusivamente para este proyecto academico. Los documentos y datos incluidos no representan a una institucion real.
