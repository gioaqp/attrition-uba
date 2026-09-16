"""
API de inferencia - Trabajo final M71V/M72V 02 (UBA)
Entrega 3: Despliegue para consumo.

Levantar con:
    uvicorn api.app:app --reload
Documentacion interactiva (demo):
    http://127.0.0.1:8000/docs
"""

from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "modelo_attrition.pkl"

app = FastAPI(
    title="Prediccion de Attrition de empleados",
    description="Sirve el pipeline entrenado (preprocesamiento + modelo) como endpoint de inferencia.",
    version="1.0.0",
)

# El artefacto se carga UNA sola vez al arrancar el proceso, no en cada request.
# Es el mismo Pipeline serializado en la Entrega 2: preprocesamiento y modelo juntos,
# por lo que la transformacion en inferencia es identica a la del entrenamiento.
modelo = None


@app.on_event("startup")
def cargar_modelo() -> None:
    global modelo
    modelo = joblib.load(MODEL_PATH)


class Empleado(BaseModel):
    """Features crudas de un empleado, tal como vienen en el dataset original."""

    Age: int
    BusinessTravel: str
    DailyRate: int
    Department: str
    DistanceFromHome: int
    Education: int
    EducationField: str
    EnvironmentSatisfaction: int
    Gender: str
    HourlyRate: int
    JobInvolvement: int
    JobLevel: int
    JobRole: str
    JobSatisfaction: int
    MaritalStatus: str
    MonthlyIncome: int
    MonthlyRate: int
    NumCompaniesWorked: int
    OverTime: str
    PercentSalaryHike: int
    PerformanceRating: int
    RelationshipSatisfaction: int
    StockOptionLevel: int
    TotalWorkingYears: int
    TrainingTimesLastYear: int
    WorkLifeBalance: int
    YearsAtCompany: int
    YearsInCurrentRole: int
    YearsSinceLastPromotion: int
    YearsWithCurrManager: int

    model_config = {
        "json_schema_extra": {
            "example": {
                  "Age": 41,
                  "BusinessTravel": "Travel_Rarely",
                  "DailyRate": 1102,
                  "Department": "Sales",
                  "DistanceFromHome": 1,
                  "Education": 2,
                  "EducationField": "Life Sciences",
                  "EnvironmentSatisfaction": 2,
                  "Gender": "Female",
                  "HourlyRate": 94,
                  "JobInvolvement": 3,
                  "JobLevel": 2,
                  "JobRole": "Sales Executive",
                  "JobSatisfaction": 4,
                  "MaritalStatus": "Single",
                  "MonthlyIncome": 5993,
                  "MonthlyRate": 19479,
                  "NumCompaniesWorked": 8,
                  "OverTime": "Yes",
                  "PercentSalaryHike": 11,
                  "PerformanceRating": 3,
                  "RelationshipSatisfaction": 1,
                  "StockOptionLevel": 0,
                  "TotalWorkingYears": 8,
                  "TrainingTimesLastYear": 0,
                  "WorkLifeBalance": 1,
                  "YearsAtCompany": 6,
                  "YearsInCurrentRole": 4,
                  "YearsSinceLastPromotion": 0,
                  "YearsWithCurrManager": 5
                }
        }
    }


class Prediccion(BaseModel):
    attrition: str = Field(description="Clase predicha: Yes o No")
    probabilidad: float = Field(description="Probabilidad de la clase positiva (Yes)")


@app.get("/health")
def health() -> dict:
    """Chequeo de vida del servicio."""
    return {"status": "ok", "modelo_cargado": modelo is not None}


@app.post("/predict", response_model=Prediccion)
def predict(empleado: Empleado) -> Prediccion:
    """Predice si un empleado va a renunciar."""
    if modelo is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")

    df = pd.DataFrame([empleado.model_dump()])
    try:
        proba = float(modelo.predict_proba(df)[0][1])
        clase = modelo.predict(df)[0]
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Error de inferencia: {exc}")

    clase = "Yes" if str(clase) in ("Yes", "1") else "No"
    return Prediccion(attrition=clase, probabilidad=round(proba, 4))


@app.post("/predict_batch", response_model=list[Prediccion])
def predict_batch(empleados: list[Empleado]) -> list[Prediccion]:
    """Igual que /predict pero para varios empleados en una sola llamada."""
    if modelo is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")

    df = pd.DataFrame([e.model_dump() for e in empleados])
    probas = modelo.predict_proba(df)[:, 1]
    clases = modelo.predict(df)

    return [
        Prediccion(
            attrition="Yes" if str(c) in ("Yes", "1") else "No",
            probabilidad=round(float(p), 4),
        )
        for c, p in zip(clases, probas)
    ]
