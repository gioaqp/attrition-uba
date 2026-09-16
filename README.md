# Predicción de renuncias de empleados (IBM HR Analytics)

Trabajo final · **M71V/M72V 02 · Implementación de Modelos de Aprendizaje Automático** · UBA, Cohorte Septiembre 2025
Alumno: **Giovanni Raffo**

Un modelo que estima, para cada empleado, la probabilidad de que renuncie, y una API local que lo sirve. El dataset es el asignado por el profesor: *IBM HR Analytics Employee Attrition & Performance* (Kaggle), 1.470 empleados, 35 columnas, 16 % de renuncias.

## Entregas

| Entrega | Qué contiene | Abrir en Colab | Estado |
|---|---|---|---|
| 1. Preparación de los datos | `notebooks/01_datos.ipynb` | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gioaqp/attrition-uba/blob/main/notebooks/01_datos.ipynb) | lista |
| 2. Entrenamiento del modelo | `notebooks/02_modelo.ipynb` | próximamente | en curso |
| 3. Despliegue para consumo | `api/` | próximamente | pendiente |

## Verlo sin instalar nada

- **Colab:** botón de la tabla y luego *Entorno de ejecución → Ejecutar todo*. La primera celda descarga este repositorio e instala lo necesario. Tarda alrededor de un minuto.
- **Solo leer:** `reports/01_datos.html` es el cuaderno con todas sus salidas; `reports/eda_sweetviz.html` es el reporte automático de exploración.

## Correrlo en la computadora

Requiere [uv](https://docs.astral.sh/uv/). Desde la carpeta del proyecto:

```powershell
uv venv .venv --python 3.11
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

Abrir los cuadernos con doble clic en `abrir_cuadernos.bat`, o ejecutarlos de punta a punta:

```powershell
.venv\Scripts\jupyter nbconvert --to notebook --execute --inplace notebooks\01_datos.ipynb
```

Quien use conda puede crear el entorno con `environment.yml`, que instala las mismas versiones.

## Estructura

```
attrition-uba/
├── data/                   dataset original y, en procesado/, el dataset final de la Entrega 1
├── notebooks/              un cuaderno por entrega
├── reports/                versiones HTML de los cuadernos y reporte Sweetviz
├── models/                 modelo entrenado (Entrega 2)
├── api/                    servicio de predicción (Entrega 3)
├── requirements.txt        versiones exactas del entorno
```

## Métricas finales

Se completan con la Entrega 2.
