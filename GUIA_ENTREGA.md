# Guia de entrega del Challenge Alura Agente

## 1. Revisar el contenido descargado

Descomprime el archivo y verifica que exista la carpeta `smartcampus-ai`. No publiques el archivo `.env` ni claves de acceso.

## 2. Probar el proyecto localmente

Abre una terminal dentro de la carpeta del proyecto.

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
streamlit run app/main.py
```

La aplicacion debe abrirse en `http://localhost:8501`. Primero prueba sin clave. Luego agrega una clave compatible en `.env` para obtener respuestas redactadas por el modelo.

## 3. Realizar pruebas funcionales

Prueba al menos estas preguntas:

1. ¿Cual es la nota minima para aprobar?
2. ¿Como recupero mi contraseña?
3. ¿Cuanto tarda un reembolso aprobado?
4. ¿Que cursos duran diez semanas?
5. ¿Cual es el curso mas economico?
6. ¿Que datos personales recopila SmartCampus?
7. ¿En cuanto tiempo debe calificarse una tarea?

Confirma que la respuesta coincida con los documentos y que las fuentes aparezcan en pantalla.

## 4. Crear el repositorio en GitHub

1. Inicia sesion en GitHub.
2. Selecciona New repository.
3. Usa el nombre `smartcampus-ai`.
4. Selecciona Public.
5. No agregues README, licencia ni gitignore desde GitHub, porque ya estan incluidos.
6. Crea el repositorio.

## 5. Subir el proyecto con historial de commits

Desde la carpeta del proyecto ejecuta:

```bash
git init
git add README.md LICENSE .gitignore
git commit -m "Initial project documentation"

git add documents
git commit -m "Add SmartCampus knowledge documents"

git add app requirements.txt .env.example tests
git commit -m "Implement document search agent"

git add Dockerfile docker-compose.yml
git commit -m "Add Docker deployment configuration"

git add screenshots/README.md GUIA_ENTREGA.md
git commit -m "Add delivery instructions and evidence folder"
```

Conecta el repositorio y publica:

```bash
git branch -M main
git remote add origin https://github.com/TU_USUARIO/smartcampus-ai.git
git push -u origin main
```

Reemplaza `TU_USUARIO` por tu nombre de usuario.

## 6. Desplegar en OCI Compute

### Crear la instancia

1. Ingresa a Oracle Cloud.
2. Abre Compute > Instances.
3. Crea una instancia Ubuntu.
4. Descarga o selecciona una clave SSH.
5. Anota la direccion IP publica.

### Abrir el puerto

En la red virtual agrega una regla de ingreso:

- Protocolo: TCP
- Puerto de destino: 8501
- Origen: `0.0.0.0/0`

Para una demostracion academica puede utilizarse ese origen. Cuando no necesites publicar la aplicacion, detén la instancia o restringe el acceso.

### Conectarse a la instancia

```bash
ssh -i TU_CLAVE.key ubuntu@IP_PUBLICA
```

### Instalar herramientas

```bash
sudo apt update
sudo apt install -y git docker.io docker-compose-v2
sudo usermod -aG docker $USER
exit
```

Vuelve a conectarte por SSH para aplicar el grupo de Docker.

### Descargar y ejecutar

```bash
git clone https://github.com/TU_USUARIO/smartcampus-ai.git
cd smartcampus-ai
cp .env.example .env
nano .env
```

Completa la clave y guarda el archivo. Luego ejecuta:

```bash
docker compose up -d --build
docker compose ps
```

Abre en el navegador:

```text
http://IP_PUBLICA:8501
```

Si la aplicacion no abre, verifica la regla del puerto y el firewall del sistema:

```bash
sudo ufw allow 8501/tcp
```

## 7. Registrar evidencia

Toma una captura donde se vea:

- La aplicacion abierta desde la IP publica.
- Una pregunta realizada.
- La respuesta y las fuentes consultadas.

Guarda la captura como `screenshots/deploy-oci.png`.

Actualiza en `README.md`:

- URL publica.
- Fecha del despliegue.
- Nombre de la captura.

Luego publica la evidencia:

```bash
git add README.md screenshots/deploy-oci.png
git commit -m "Add OCI deployment evidence"
git push
```

## 8. Revisar el repositorio

Antes de enviar, verifica:

- El repositorio es publico.
- El README se muestra correctamente.
- Los PDFs y el CSV pueden abrirse.
- El codigo fuente esta incluido.
- Existe un historial de varios commits.
- No existe un archivo `.env` en GitHub.
- No hay claves ni contraseñas publicadas.
- La URL de OCI funciona.
- La captura del despliegue esta visible.

## 9. Entregar en Alura

1. Copia la URL publica del repositorio.
2. Pega la URL en el formulario del Challenge.
3. Selecciona la autorizacion de uso pedagogico segun tu preferencia.
4. Descarga el badge cuando la plataforma lo solicite.
5. Revisa nuevamente la URL.
6. Selecciona Enviar proyecto.

La entrega admite cinco intentos. Utiliza el primer intento solo cuando el repositorio y la evidencia ya esten completos.
