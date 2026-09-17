from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

MODELO = Path(__file__).resolve().parent.parent / "models" / "modelo_attrition.pkl"

modelo = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    modelo["pipeline"] = joblib.load(MODELO)
    yield
    modelo.clear()


app = FastAPI(
    title="Predicción de renuncias",
    description="Recibe los datos de un empleado y devuelve la probabilidad de que renuncie.",
    version="1.0",
    lifespan=lifespan,
)


class Empleado(BaseModel):
    Age: int
    BusinessTravel: Literal["Non-Travel", "Travel_Frequently", "Travel_Rarely"]
    DailyRate: int
    Department: Literal["Human Resources", "Research & Development", "Sales"]
    DistanceFromHome: int
    Education: int
    EducationField: Literal[
        "Human Resources",
        "Life Sciences",
        "Marketing",
        "Medical",
        "Other",
        "Technical Degree",
    ]
    EnvironmentSatisfaction: int
    Gender: Literal["Female", "Male"]
    HourlyRate: int
    JobInvolvement: int
    JobRole: Literal[
        "Healthcare Representative",
        "Human Resources",
        "Laboratory Technician",
        "Manager",
        "Manufacturing Director",
        "Research Director",
        "Research Scientist",
        "Sales Executive",
        "Sales Representative",
    ]
    JobSatisfaction: int
    MaritalStatus: Literal["Divorced", "Married", "Single"]
    MonthlyIncome: int
    MonthlyRate: int
    NumCompaniesWorked: int
    OverTime: Literal["No", "Yes"]
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
                "Age": 21,
                "BusinessTravel": "Travel_Frequently",
                "DailyRate": 756,
                "Department": "Sales",
                "DistanceFromHome": 1,
                "Education": 1,
                "EducationField": "Technical Degree",
                "EnvironmentSatisfaction": 1,
                "Gender": "Female",
                "HourlyRate": 99,
                "JobInvolvement": 2,
                "JobRole": "Sales Representative",
                "JobSatisfaction": 2,
                "MaritalStatus": "Single",
                "MonthlyIncome": 2174,
                "MonthlyRate": 9150,
                "NumCompaniesWorked": 1,
                "OverTime": "Yes",
                "PercentSalaryHike": 11,
                "PerformanceRating": 3,
                "RelationshipSatisfaction": 3,
                "StockOptionLevel": 0,
                "TotalWorkingYears": 1,
                "TrainingTimesLastYear": 3,
                "WorkLifeBalance": 3,
                "YearsAtCompany": 1,
                "YearsInCurrentRole": 0,
                "YearsSinceLastPromotion": 0,
                "YearsWithCurrManager": 0,
            }
        }
    }


class Respuesta(BaseModel):
    attrition: str
    probabilidad: float


@app.get("/health")
def health():
    return {"estado": "ok", "modelo_cargado": "pipeline" in modelo}


@app.post("/predict", response_model=Respuesta)
def predict(empleado: Empleado):
    datos = pd.DataFrame([empleado.model_dump()])
    pipeline = modelo["pipeline"]
    probabilidad = float(pipeline.predict_proba(datos)[0][1])
    renuncia = int(pipeline.predict(datos)[0]) == 1
    return Respuesta(
        attrition="Yes" if renuncia else "No",
        probabilidad=round(probabilidad, 4),
    )
