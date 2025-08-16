from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

# --- 1. Modelos de Datos (Data Models) ---
# Modelo para cada objeto de inversión en la entrada
class ObjetoInversion(BaseModel):
    nombre: str
    peso: int = Field(..., gt=0)  # gt=0 asegura que el costo sea positivo
    ganancia: int = Field(..., gt=0) # gt=0 asegura que la ganancia sea positiva

# Modelo para el JSON de entrada (request body)
class EntradaOptimizar(BaseModel):
    capacidad: int = Field(..., gt=0) # gt=0 asegura que la capacidad sea positiva
    objetos: List[ObjetoInversion]

# Modelo para el JSON de salida (response body)
class SalidaOptimizar(BaseModel):
    seleccionados: List[str]
    ganancia_total: int
    peso_total: int

# --- 2. Lógica del Algoritmo (Algorithm Logic) ---
# Algoritmo de Knapsack con Programación Dinámica
def optimizar_portafolio(capacidad: int, objetos: List[ObjetoInversion]):
    n = len(objetos)
    # Creamos la tabla de programación dinámica
    # dp[i][w] almacenará la máxima ganancia para una capacidad 'w' usando los primeros 'i' objetos
    dp = [[0 for _ in range(capacidad + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacidad + 1):
            # Obtenemos el peso (costo) y la ganancia del objeto actual
            peso_actual = objetos[i-1].peso
            ganancia_actual = objetos[i-1].ganancia

            # Si el objeto actual es más pesado que la capacidad actual, no podemos incluirlo
            if peso_actual > w:
                dp[i][w] = dp[i-1][w]
            else:
                # Comparamos dos escenarios:
                # 1. No incluir el objeto actual: la ganancia es la misma que antes (dp[i-1][w])
                # 2. Incluir el objeto actual: la ganancia es la ganancia del objeto + la máxima ganancia
                #    que se podía obtener con el resto de la capacidad (w - peso_actual)
                dp[i][w] = max(dp[i-1][w], ganancia_actual + dp[i-1][w - peso_actual])

    # --- Reconstruir la solución para saber qué objetos se seleccionaron ---
    ganancia_total = dp[n][capacidad]
    peso_total = 0
    seleccionados_nombres = []
    w = capacidad

    for i in range(n, 0, -1):
        # Si la ganancia en la fila actual es diferente a la anterior, significa que el objeto i fue incluido
        if dp[i][w] != dp[i-1][w]:
            objeto_actual = objetos[i-1]
            seleccionados_nombres.append(objeto_actual.nombre)
            w -= objeto_actual.peso
            peso_total += objeto_actual.peso
    
    # Los objetos se encuentran en orden inverso, así que los revertimos
    seleccionados_nombres.reverse()

    return seleccionados_nombres, ganancia_total, peso_total


# --- 3. Creación de la App y el Endpoint ---
app = FastAPI(
    title="API de Optimización de Portafolio",
    description="Un microservicio que resuelve el problema de la mochila (knapsack) para optimizar un portafolio de inversiones.",
    version="1.0.0",
)

# --- Configuración de CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)

@app.post("/optimizar", response_model=SalidaOptimizar)
async def endpoint_optimizar(entrada: EntradaOptimizar):
    """
    Recibe una capacidad de presupuesto y una lista de oportunidades de inversión.
    Devuelve la combinación óptima que maximiza la ganancia sin superar el presupuesto.
    """
    nombres, ganancia, peso = optimizar_portafolio(entrada.capacidad, entrada.objetos)
    
    return SalidaOptimizar(
        seleccionados=nombres,
        ganancia_total=ganancia,
        peso_total=peso
    )

# --- 4. (Opcional) Comando para correr la app ---
# Para ejecutar la aplicación, guarda este archivo como main.py y corre en la terminal:
# uvicorn main:app --reload
