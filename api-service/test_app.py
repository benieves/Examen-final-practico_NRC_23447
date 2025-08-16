import pytest
from fastapi.testclient import TestClient
from main import app

# Creamos un cliente de prueba para la aplicación
client = TestClient(app)

# --- Casos de Éxito (Basados en el PDF) ---

def test_caso_exito_1():
    """
    Prueba el Caso de Éxito 1 del PDF.
    Combinación óptima dentro del límite.
    """
    response = client.post("/optimizar", json={
        "capacidad": 10000,
        "objetos": [
            {"nombre": "Fondo_A", "peso": 2000, "ganancia": 1500},
            {"nombre": "Fondo_B", "peso": 4000, "ganancia": 3500},
            {"nombre": "Fondo_C", "peso": 5000, "ganancia": 4000},
            {"nombre": "Fondo_D", "peso": 3000, "ganancia": 2500},
            {"nombre": "Fondo_E", "peso": 1500, "ganancia": 1800}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    # Ordenamos las listas para que la comparación no falle por el orden
    assert sorted(data["seleccionados"]) == sorted(["Fondo_B", "Fondo_C", "Fondo_E"])
    assert data["ganancia_total"] == 9300
    assert data["peso_total"] == 10000

def test_caso_exito_2():
    """
    Prueba el Caso de Éxito 2 del PDF.
    Máximo aprovechamiento de capacidad.
    """
    response = client.post("/optimizar", json={
        "capacidad": 8000,
        "objetos": [
            {"nombre": "Accion_X", "peso": 1000, "ganancia": 800},
            {"nombre": "Accion_Y", "peso": 2500, "ganancia": 2200},
            {"nombre": "Accion_Z", "peso": 3000, "ganancia": 2800},
            {"nombre": "Bono_P", "peso": 4000, "ganancia": 3000},
            {"nombre": "Bono_Q", "peso": 1500, "ganancia": 1200}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert sorted(data["seleccionados"]) == sorted(["Accion_Y", "Accion_Z", "Bono_Q"])
    assert data["ganancia_total"] == 6200
    assert data["peso_total"] == 7000

def test_caso_exito_3():
    """
    Prueba el Caso de Éxito 3 del PDF.
    Proyectos de bajo costo, alta rentabilidad.
    """
    response = client.post("/optimizar", json={
        "capacidad": 5000,
        "objetos": [
            {"nombre": "Cripto_1", "peso": 500, "ganancia": 700},
            {"nombre": "Cripto_2", "peso": 800, "ganancia": 1000},
            {"nombre": "ETF_1", "peso": 1500, "ganancia": 1300},
            {"nombre": "ETF_2", "peso": 2000, "ganancia": 1800},
            {"nombre": "NFT_Alpha", "peso": 3000, "ganancia": 2500}
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert sorted(data["seleccionados"]) == sorted(["Cripto_1", "Cripto_2", "ETF_1", "ETF_2"])
    assert data["ganancia_total"] == 4800
    assert data["peso_total"] == 4800


# --- Casos de Error y Casos Límite ---

def test_error_capacidad_negativa():
    """
    Prueba que la API rechace una capacidad negativa.
    Debe devolver un error 422 Unprocessable Entity.
    """
    response = client.post("/optimizar", json={
        "capacidad": -100,
        "objetos": [{"nombre": "A", "peso": 1, "ganancia": 1}]
    })
    assert response.status_code == 422

def test_error_peso_cero():
    """
    Prueba que la API rechace un objeto con peso cero.
    Debe devolver un error 422.
    """
    response = client.post("/optimizar", json={
        "capacidad": 100,
        "objetos": [{"nombre": "A", "peso": 0, "ganancia": 1}]
    })
    assert response.status_code == 422

def test_limite_capacidad_cero():
    """
    Prueba el caso límite donde la capacidad es cero.
    No se debe seleccionar ningún objeto.
    """
    response = client.post("/optimizar", json={
        "capacidad": 0,
        "objetos": [{"nombre": "A", "peso": 10, "ganancia": 10}]
    })
    # La validación gt=0 (mayor que 0) en el modelo Pydantic rechazará esto.
    assert response.status_code == 422

def test_limite_sin_objetos():
    """
    Prueba el caso límite donde la lista de objetos está vacía.
    """
    response = client.post("/optimizar", json={
        "capacidad": 1000,
        "objetos": []
    })
    assert response.status_code == 200
    data = response.json()
    assert data["seleccionados"] == []
    assert data["ganancia_total"] == 0
    assert data["peso_total"] == 0
