# Optimizador de Portafolio de Inversiones

Este proyecto implementa un microservicio para optimizar un portafolio de inversiones utilizando un algoritmo de programación dinámica (problema de la mochila 0/1), junto con una interfaz web sencilla para interactuar con él.

## Estructura del Proyecto

```
Examen-final-practico_NRC_23447/
├── api-service/
│   ├── app.py             # Lógica del microservicio (FastAPI)
│   ├── requirements.txt    # Dependencias de Python
│   ├── test_app.py        # Pruebas unitarias para el backend
│   └── Dockerfile          # Configuración para Docker
├── web-client/
│   ├── index.html          # Interfaz de usuario (HTML)
│   ├── style.css           # Estilos de la interfaz (CSS)
│   └── script.js           # Lógica de la interfaz (JavaScript)
└── README.md               # Este archivo
```

## Requisitos

*   **Python 3.9+**
*   **pip** (gestor de paquetes de Python)
*   **Node.js y npm** (opcional, si se desea usar un servidor local para el frontend)
*   **Docker** (opcional, para ejecutar el backend en un contenedor)

## Despliegue y Ejecución

Sigue estos pasos para poner en marcha el proyecto.

### 1. Backend (Microservicio)

El microservicio está construido con FastAPI.

#### A. Configuración del Entorno Virtual e Instalación de Dependencias

1.  Navega al directorio `api-service`:
    ```bash
    cd Examen-final-practico_NRC_23447/api-service
    ```
2.  Crea un entorno virtual (si no lo has hecho ya):
    ```bash
    python -m venv venv
    ```
3.  Activa el entorno virtual:
    *   **Windows (Command Prompt):** `venv\Scripts\activate`
    *   **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`
    *   **Linux/macOS:** `source venv/bin/activate`
4.  Instala las dependencias de Python:
    ```bash
    pip install -r requirements.txt
    ```

#### B. Ejecutar el Microservicio

Con el entorno virtual activado, ejecuta el servidor Uvicorn:

```bash
uvicorn app:app --reload
```

El microservicio estará disponible en `http://127.0.0.1:8000`. Puedes acceder a la documentación interactiva de la API en `http://127.0.0.1:8000/docs`.

#### C. Ejecutar Pruebas del Backend

Con el entorno virtual activado y en el directorio `api-service`, ejecuta:

```bash
pytest
```

### 2. Frontend (Interfaz Web)

La interfaz web es una aplicación de HTML, CSS y JavaScript puro.

#### A. Ejecutar la Interfaz Web

Para evitar problemas de CORS al abrir `index.html` directamente desde el navegador, se recomienda servir el frontend usando un servidor web local.

1.  Navega al directorio `web-client`:
    ```bash
    cd Examen-final-practico_NRC_23447/web-client
    ```
2.  Inicia un servidor HTTP simple de Python:
    ```bash
    python -m http.server 8001
    ```
    (Si no tienes Python, puedes usar `npx http-server` si tienes Node.js, o cualquier otro servidor web local).

3.  Abre tu navegador y visita `http://localhost:8001`.

### 3. Ejecución con Docker (Solo Backend)

Si tienes Docker instalado, puedes construir y ejecutar el microservicio en un contenedor.

1.  Navega al directorio `api-service`:
    ```bash
    cd Examen-final-practico_NRC_23447/api-service
    ```
2.  Construye la imagen Docker:
    ```bash
    docker build -t investment-optimizer-api .
    ```
3.  Ejecuta el contenedor Docker:
    ```bash
    docker run -p 8000:8000 investment-optimizer-api
    ```
    El microservicio estará disponible en `http://localhost:8000`.

## Ejemplos de Uso de la API

El endpoint principal es `POST /optimizar`.

### Request Body (JSON)

```json
{
  "capacidad": 10000,
  "objetos": [
    {"nombre": "Fondo_A", "peso": 2000, "ganancia": 1500},
    {"nombre": "Fondo_B", "peso": 4000, "ganancia": 3500},
    {"nombre": "Fondo_C", "peso": 5000, "ganancia": 4000},
    {"nombre": "Fondo_D", "peso": 3000, "ganancia": 2500},
    {"nombre": "Fondo_E", "peso": 1500, "ganancia": 1800}
  ]
}
```

### Response Body (JSON)

```json
{
  "seleccionados": ["Fondo_B", "Fondo_C", "Fondo_E"],
  "ganancia_total": 9300,
  "peso_total": 10000
}
```

## Dependencias del Proyecto

### Backend

*   **FastAPI**: Framework web para construir APIs.
*   **Uvicorn**: Servidor ASGI para ejecutar aplicaciones FastAPI.
*   **Pydantic**: Para la validación de datos y la definición de modelos.
*   **httpx**: Cliente HTTP para pruebas asíncronas.
*   **pytest**: Framework de pruebas.

### Frontend

*   **HTML5**
*   **CSS3**
*   **JavaScript (ES6+)**
